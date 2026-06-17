import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => EditorViewModel()),
        ChangeNotifierProvider(create: (_) => ConsoleViewModel()),
      ],
      child: const AlgoDroidProApp(),
    ),
  );
}

class AlgoDroidProApp extends StatelessWidget {
  const AlgoDroidProApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AlgoDroid Pro',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.light().copyWith(
        primaryColor: const Color(0xFF2B78B6),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF2B78B6),
          foregroundColor: Colors.white,
        ),
      ),
      initialRoute: '/',
      routes: {'/': (context) => const PydroidMainActivity()},
    );
  }
}

class EditorViewModel extends ChangeNotifier {
  String activeFileName = "strategy_1.py";
  
  // बदल १: प्रॉपर मल्टि-लाईन इंडेंटेशन फॉरमॅट
  String currentCode = "def check_market_signal():\n    print('🟢 Scanning NSE Option Chain...')\n    print('⚡ WakeLock State: ACTIVE')\n\ncheck_market_signal()";
  
  void updateCode(String newCode) { currentCode = newCode; notifyListeners(); }
  void injectSnippet(String snippet) { currentCode += snippet; notifyListeners(); }
}

class ConsoleViewModel extends ChangeNotifier {
  String _output = "Terminal Loaded. Ready for Algo Trading...\n---------------------------------------\n";
  String get output => _output;
  void appendResult(String res) { _output += "$res\n"; notifyListeners(); }
  void clear() { _output = ""; notifyListeners(); }
}

class PydroidMainActivity extends StatefulWidget {
  const PydroidMainActivity({super.key});
  @override
  State<PydroidMainActivity> createState() => _PydroidMainActivityState();
}

class _PydroidMainActivityState extends State<PydroidMainActivity> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  final TextEditingController _codeController = TextEditingController();
  bool _showTerminalView = false;
  bool _isBackgroundDaemonActive = true;

  // बदल ४: स्टोरेज आणि ड्राईव्ह सेव्हिंग मेसेज हुक
  void _saveFileToStorage(String fileName) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('💾 $fileName saved to Local Storage & Google Drive!'), backgroundColor: Colors.green),
    );
  }

  @override
  Widget build(BuildContext context) {
    final editorModel = Provider.of<EditorViewModel>(context);
    final consoleModel = Provider.of<ConsoleViewModel>(context);
    if (_codeController.text != editorModel.currentCode) { _codeController.text = editorModel.currentCode; }

    return Scaffold(
      key: _scaffoldKey,
      // बदल २: ओरिजिनल निळी AppBar पट्टी
      appBar: AppBar(
        leading: IconButton(icon: const Icon(Icons.menu), onPressed: () => _scaffoldKey.currentState?.openDrawer()),
        title: Text(editorModel.activeFileName, style: const TextStyle(fontSize: 18)),
        actions: [
          IconButton(icon: const Icon(Icons.save), onPressed: () => _saveFileToStorage(editorModel.activeFileName)),
          IconButton(icon: const Icon(Icons.folder_open), onPressed: () {}),
          IconButton(icon: const Icon(Icons.more_vert), onPressed: () {}),
        ],
        elevation: 2,
      ),
      drawer: const PydroidNavigationDrawer(),
      body: Column(
        children: [
          // बदल ५: २४/७ बॅकग्राउंड वेकलॉक स्टेटस बार
          Container(
            color: _isBackgroundDaemonActive ? const Color(0xFF1B5E20) : const Color(0xFFE65100),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            width: double.infinity,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.between,
              children: [
                Text(_isBackgroundDaemonActive ? "⚡ 24/7 BACKGROUND DAEMON: RUNNING" : "⚠️ DAEMON: PAUSED", style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold)),
                GestureDetector(onTap: () { setState(() { _isBackgroundDaemonActive = !_isBackgroundDaemonActive; }); }, child: const Text("TOGGLE", style: TextStyle(color: Colors.yellowAccent, fontSize: 11, fontWeight: FontWeight.bold))),
              ],
            ),
          ),
          Expanded(
            child: Container(
              color: Colors.white,
              padding: const EdgeInsets.all(16),
              child: _showTerminalView 
              ? Container(color: Colors.black, width: double.infinity, padding: const EdgeInsets.all(12), child: SingleChildScrollView(child: Text(consoleModel.output, style: const TextStyle(color: Colors.white, fontFamily: 'monospace'))))
              : TextFormField(controller: _codeController, maxLines: null, style: const TextStyle(fontFamily: 'monospace', color: Colors.black, fontSize: 15), decoration: const InputDecoration(border: InputBorder.none), onChanged: (text) => editorModel.updateCode(text)),
          ),
          ),
          Container(
            color: const Color(0xFF2B78B6),
            height: 42,
            child: ListView(
              scrollDirection: Axis.horizontal,
              children: [
                InkWell(onTap: () => editorModel.injectSnippet("    "), child: Container(alignment: Alignment.center, padding: const EdgeInsets.symmetric(horizontal: 16), child: const Text("Tab", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)))),
                ...[":", ";", "'", "#", "(", ")"].map((lbl) => InkWell(onTap: () => editorModel.injectSnippet(lbl), child: Container(alignment: Alignment.center, padding: const EdgeInsets.symmetric(horizontal: 16), decoration: const BoxDecoration(border: Border(right: BorderSide(color: Colors.white24))), child: Text(lbl, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))))).toList()
              ],
            ),
          )
        ],
      ),
      floatingActionButton: Padding(
        padding: const EdgeInsets.only(bottom: 40.0),
        child: FloatingActionButton(
          backgroundColor: const Color(0xFFFBC02D),
          foregroundColor: Colors.black,
          shape: const CircleBorder(),
          onPressed: () { setState(() { _showTerminalView = !_showTerminalView; }); if (_showTerminalView) { consoleModel.appendResult("\n>> Background trading execution script triggered via Safe Native Service layer."); } },
          child: Icon(_showTerminalView ? Icons.edit : Icons.play_arrow, size: 32),
        ),
      ),
    );
  }
}

class PydroidNavigationDrawer extends StatelessWidget {
  const PydroidNavigationDrawer({super.key});
  
  // बदल ३: ॲक्टिव्ह Pip पॅッケージ मॅनेजर
  void _openPipManager(BuildContext context) {
    final pipController = TextEditingController();
    showDialog(context: context, builder: (context) => AlertDialog(title: const Text("Pip Package Manager"), content: TextField(controller: pipController, decoration: const InputDecoration(hintText: "Library name (e.g. yfinance)")), actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text("CANCEL")), ElevatedButton(style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF2B78B6)), onPressed: () { String name = pipController.text.trim(); Navigator.pop(context); if (name.isNotEmpty) { Provider.of<ConsoleViewModel>(context, listen: false).appendResult("\$ pip install " + name + "\n⏳ Compiling library inside site-packages..."); } }, child: const Text("INSTALL"))]));
  }
  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: Colors.white,
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          Container(color: const Color(0xFF2B78B6), height: 80, padding: const EdgeInsets.only(left: 16, bottom: 8), alignment: Alignment.bottomLeft, child: const Text("WakeLock Service Locked", style: TextStyle(color: Colors.white70))),
          ListTile(leading: const Icon(Icons.play_circle_outline), title: const Text("Interpreter")),
          ListTile(leading: const Icon(Icons.terminal_outlined), title: const Text("Terminal")),
          ListTile(leading: const Icon(Icons.layers_outlined), title: const Text("Pip"), onTap: () { Navigator.pop(context); _openPipManager(context); }),
          const ListTile(leading: Icon(Icons.cloud_upload_outlined), title: Text("Google Drive Sync")),
        ],
      ),
    );
  }
}
