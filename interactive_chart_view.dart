import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class InteractiveChartView extends StatefulWidget {
  const InteractiveChartView({super.key});

  @override
  State<InteractiveChartView> createState() => _InteractiveChartViewState();
}

class _InteractiveChartViewState extends State<InteractiveChartView> {
  late final WebViewController _webController;

  @override
  void initState() {
    super.initState();
    
    // नियम १४: अंतर्गत मायक्रो-लोकलहोस्ट किंवा HTML स्ट्रिंग प्रवेगक (Webview Acceleration)
    _webController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0xFF121212))
      ..loadHtmlString(_getPlotlyHtmlMarketTemplate());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Live Technical Analytics", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF1E1E1E),
      ),
      body: WebViewWidget(controller: _webController),
    );
  }

  // नियम ९: Plotly Candlestick & Order-Flow Visualizer Template
  String _getPlotlyHtmlMarketTemplate() {
    return '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
      <style>
        body { background-color: #121212; margin: 0; padding: 4px; font-family: sans-serif; color: #fff; }
        #chart { width: 100vw; height: 85vh; }
      </style>
    </head>
    <body>
      <div id="chart"></div>
      <script>
        // लाइव्ह सीवीडी (CVD) आणि स्मार्ट मनी कन्सेप्ट्स (SMC) साठी मॉक डेटा सि्युलेशन
        var trace = {
          x: ['2026-06-15 10:00', '2026-06-15 11:00', '2026-06-15 12:00', '2026-06-15 13:00', '2026-06-15 14:00'],
          close: [23400, 23450, 23420, 23510, 23490],
          high: [23450, 23490, 23460, 23550, 23520],
          low: [23380, 23410, 23390, 23400, 23460],
          open: [23390, 23410, 23440, 23420, 23510],
          type: 'candlestick',
          xaxis: 'x', yaxis: 'y'
        };

        var layout = {
          dragmode: 'zoom',
          showlegend: false,
          paper_bgcolor: '#121212',
          plot_bgcolor: '#121212',
          margin: { r: 10, t: 10, b: 40, l: 40 },
          xaxis: { gridcolor: '#222', rangeslider: {visible: false} },
          yaxis: { gridcolor: '#222' }
        };

        Plotly.newPlot('chart', [trace], layout);
      </script>
    </body>
    </html>
    ''';
  }
}
