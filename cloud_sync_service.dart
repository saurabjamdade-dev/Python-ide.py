import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class CloudSyncService {
  final String githubToken = "ghp_SecureGitHubTokenInjectedFromVault";
  final String repoOwner = "saurabjamdade-dev";
  final String repoName = "Python-ide.py";

  // नियम २०: गिटहब ऑटो-कमिट सिस्टीम (GitHub Auto Commit System)
  Future<bool> autoCommitToGitHub({
    required String fileName,
    required String fileContent,
    required String commitMessage,
  }) async {
    final String url = 'https://api.github.com/repos/$repoOwner/$repoName/contents/$fileName';
    
    try {
      // फाईल आधीपासून अस्तित्वात आहे का हे तपासण्यासाठी SHA मिळवणे
      final getResponse = await http.get(
        Uri.parse(url),
        headers: {'Authorization': 'token $githubToken', 'Accept': 'application/vnd.github.v3+json'},
      );

      String? sha;
      if (getResponse.statusCode == 200) {
        final decoded = jsonDecode(getResponse.body);
        sha = decoded['sha'];
      }

      // नियम ५ नुसार सुरक्षित बेस६४ एन्कोडिंग (Base64 Safe Mode)
      final String base64Content = base64Encode(utf8.encode(fileContent));

      final response = await http.put(
        Uri.parse(url),
        headers: {
          'Authorization': 'token $githubToken',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          "message": commitMessage,
          "content": base64Content,
          if (sha != null) "sha": sha
        }),
      );

      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      return false;
    }
  }

  // नियम २४: गुगल ड्राईव्ह स्टोरेज ऑटो-बॅकअप (Google Drive Storage Sync)
  Future<bool> backupToGoogleDrive({
    required String fileName,
    required String fileContent,
    required String oauthToken,
  }) async {
    const String url = 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart';
    
    try {
      final Map<String, String> headers = {
        'Authorization': 'Bearer $oauthToken',
        'Content-Type': 'multipart/related; boundary=foo_bar_baz',
      };

      // गुगल ड्राईव्हच्या गरजेनुसार मल्टिपार्ट बॉडी स्ट्रक्चर
      final String body = '--foo_bar_baz\r\n'
          'Content-Type: application/json; charset=UTF-8\r\n\r\n'
          '{"name": "$fileName", "mimeType": "text/x-python"}\r\n'
          '--foo_bar_baz\r\n'
          'Content-Type: text/x-python\r\n\r\n'
          '$fileContent\r\n'
          '--foo_bar_baz--';

      final response = await http.post(Uri.parse(url), headers: headers, body: body);
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
