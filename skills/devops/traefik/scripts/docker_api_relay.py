#!/usr/bin/env python3
"""
Docker TCP Relay v3.0 (Traefik v3 vs Docker 29.4+ MinAPI Workaround)
Listens on TCP 2376 → forwards to unix:/var/run/docker.sock

Fixes Docker 29.4+ (which enforces MinAPIVersion=1.40) rejecting Traefik's
hardcoded HTTP negotiation which sends `GET /v1.24/version`.
Rewrites ALL HTTP requests on persistent connections (HTTP/1.1) to use /v1.40/.
"""
import socket
import threading
import re
import sys

DOCKER_SOCKET = '/var/run/docker.sock'
TCP_PORT = 2376
BUFFER_SIZE = 65536

REWRITE_PATTERN = re.compile(
    rb'(GET|POST|PUT|DELETE|PATCH|HEAD) /v1\.(2[0-9]|3[0-9]|1[0-9]|[0-9])/'
)

def process_client_data(data):
    """Rewrite all HTTP requests' API version in data chunk to 1.40"""
    def replace_version(m):
        old = m.group(0)
        new = re.sub(rb'/v1\.[0-9]+/', b'/v1.40/', old)
        if old != new:
            print(f"  Rewrite: {old.decode()[:40]} → /v1.40/", flush=True)
        return new
    return REWRITE_PATTERN.sub(replace_version, data)

def forward_with_rewrite(src, dst, rewrite=False, done_event=None):
    """Forward data, optionally rewriting client API version"""
    try:
        while True:
            try:
                data = src.recv(BUFFER_SIZE)
            except OSError:
                break
            if not data:
                break
            if rewrite:
                data = process_client_data(data)
            try:
                dst.sendall(data)
            except OSError:
                break
    except Exception:
        pass
    finally:
        if done_event:
            done_event.set()
        try:
            dst.shutdown(socket.SHUT_WR)
        except:
            pass

def handle_client(client_sock):
    """Handle one client connection with full bidirectional forwarding"""
    unix_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        unix_sock.connect(DOCKER_SOCKET)
    except Exception as e:
        print(f"Cannot connect docker socket: {e}", file=sys.stderr, flush=True)
        client_sock.close()
        return

    done = threading.Event()

    # Client → Docker (with rewrite)
    t1 = threading.Thread(
        target=forward_with_rewrite,
        args=(client_sock, unix_sock, True, done),
        daemon=True
    )
    # Docker → Client (passthrough)
    t2 = threading.Thread(
        target=forward_with_rewrite,
        args=(unix_sock, client_sock, False, None),
        daemon=True
    )

    t1.start()
    t2.start()

    done.wait(timeout=600)  # 10 min timeout for events stream

    for sock in [unix_sock, client_sock]:
        try:
            sock.close()
        except:
            pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', TCP_PORT))
    server.listen(200)
    print(f"Docker TCP Relay listening on 0.0.0.0:{TCP_PORT} → {DOCKER_SOCKET}", flush=True)

    while True:
        try:
            client, addr = server.accept()
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            threading.Thread(target=handle_client, args=(client,), daemon=True).start()
        except Exception as e:
            print(f"Accept error: {e}", file=sys.stderr, flush=True)

if __name__ == '__main__':
    main()