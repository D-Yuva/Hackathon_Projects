import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'api_service.dart'; // Import the API service file

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Image Generator',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: ImageGeneratorPage(),
    );
  }
}

class ImageGeneratorPage extends StatefulWidget {
  @override
  _ImageGeneratorPageState createState() => _ImageGeneratorPageState();
}

class _ImageGeneratorPageState extends State<ImageGeneratorPage> {
  Uint8List? _imageBytes;
  bool _isLoading = false;
  final TextEditingController _controller = TextEditingController();

  Future<void> _generateImage() async {
    final prompt = _controller.text.trim();

    if (prompt.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Please enter a prompt')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final imageBytes = await ApiService.generateImage(prompt);
      setState(() {
        _imageBytes = imageBytes;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: ${e.toString()}')),
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('AI Image Generator'),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 20),
              TextField(
                controller: _controller,
                decoration: InputDecoration(
                  labelText: 'Enter your prompt here',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.edit),
                ),
                textInputAction: TextInputAction.done,
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _generateImage,
                icon: Icon(Icons.image),
                label: Text('Generate Image'),
                style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(vertical: 12, horizontal: 20),
                  textStyle: TextStyle(fontSize: 16),
                ),
              ),
              const SizedBox(height: 20),
              _isLoading
                  ? CircularProgressIndicator()
                  : _imageBytes != null
                      ? Column(
                          children: [
                            const SizedBox(height: 20),
                            Text(
                              'Generated Image:',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 10),
                            Image.memory(_imageBytes!),
                          ],
                        )
                      : Text(
                          'No image generated yet',
                          style: TextStyle(fontSize: 16),
                        ),
            ],
          ),
        ),
      ),
    );
  }
}
