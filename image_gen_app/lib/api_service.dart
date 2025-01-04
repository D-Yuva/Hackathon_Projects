import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;

class ApiService {
  static const String _baseUrl =
      'YOUR_HUGGING_FACE_TOKEN';
  static const String _apiKey = 'API_KEY';

  static Future<Uint8List?> generateImage(String inputText) async {
    final url = Uri.parse(_baseUrl);
    final headers = {
      'Authorization': 'Bearer $_apiKey',
      'Content-Type': 'application/json',
    };
    final body = jsonEncode({'inputs': inputText});

    final response = await http.post(url, headers: headers, body: body);

    if (response.statusCode == 200) {
      return response.bodyBytes;
    } else {
      throw Exception('Failed to generate image: ${response.body}');
    }
  }
}
