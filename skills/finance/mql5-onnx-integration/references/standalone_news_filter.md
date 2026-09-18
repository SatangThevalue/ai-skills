# Decoupled Standalone News Filter in MQL5

To protect EAs from news spikes (e.g., Gold during NFP) without relying on an external Python server (which can crash or disconnect), implement a standalone news engine directly in MQL5.

## Architecture
1. **API Endpoint**: Use ForexFactory's XML (`https://nfs.faireconomy.media/ff_calendar_thisweek.xml`).
2. **MT5 Security**: User must manually add the URL to `Tools > Options > Expert Advisors > Allow WebRequest`. The EA should check this and fail gracefully with a log message if not enabled, rather than crashing.
3. **Timezone Synchronization (Crucial)**: 
   - ForexFactory XML provides times in EST/EDT or UTC.
   - MT5 broker time varies.
   - Use `TimeCurrent() - TimeGMT()` to calculate the dynamic timezone offset, ensuring the EA blocks trading exactly 30 minutes before high-impact news, regardless of the broker's server location.
4. **Rate Limiting**: EA should download the XML only once per day (or cache it in RAM) to avoid IP bans, rather than fetching on every tick.