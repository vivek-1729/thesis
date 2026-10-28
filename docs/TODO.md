# Processing queue

In order. Each item says what it unblocks, so the order is not arbitrary.

1. **Georeference the historic charts.** The keystone. Unblocks items 2, 3 and 8.
   Admiralty sheets carry a printed latitude and longitude graticule, so the
   transform can come from the chart's own grid rather than from feature
   matching against a modern map.
2. **Transcribe the Admiralty soundings.** Several thousand across nine sheets,
   against twenty held now. Needs item 1 to give each one a position.
3. **Trace shorelines from the charts** and compare against the satellite
   epochs, each as a band rather than a line.
4. **Train the terrain segmenter** and score all seven ports with it.
5. **Build the voyage simulator** on the wind climatology already gathered.
6. **Measure the Malabar distances through the backwaters** rather than in
   straight lines.
7. **Run the per-leg stadion analysis.** Needs nothing that is not in hand.
8. **Pull ICESat-2 depths**, once the Earthdata login exists.

Blocked on acquisition, not on processing: the Kerala sea level curve, the
Periyar resistivity survey, the Kuttanad boreholes, and the nine open-access
PDFs that need a browser.
