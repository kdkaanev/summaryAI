from django.test import TestCase

# Create your tests here.
class APITests(TestCase):
    VIDEO_WITH_TRANSCRIPT = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    # Примерно видео без транскрипция (измислено ID)
    VIDEO_NO_TRANSCRIPT = "https://www.youtube.com/watch?v=aaaaaaaaaaa"


    def setUp(self):
        # Set up any necessary data or state before each test
        pass

    def test_summarize_view(self):
        # Test the summarize view with a sample URL
        response = self.client.post('/api/summarize/', {'url': self.VIDEO_WITH_TRANSCRIPT})
        self.assertEqual(response.status_code, 200)
        self.assertIn('summary', response.json())

    def test_invalid_url(self):
        # Test the summarize view with an invalid URL
        response = self.client.post('/api/summarize/', {'url': 'invalid-url'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_video_without_transcript(self):
        # Test the summarize view with a video that has no transcript
        response = self.client.post('/api/summarize/', {'url': self.VIDEO_NO_TRANSCRIPT})
        self.assertEqual(response.status_code, 200)

    def test_transcript_available(self):
        transcript = self.client.post(self.VIDEO_WITH_TRANSCRIPT)
        assert isinstance(transcript, str)
        assert len(transcript) > 10  # трябва да има съдържание

