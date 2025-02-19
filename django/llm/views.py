from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI

class ChatView(APIView):
    def post(self, request):
        try:
            prompt = request.data.get('prompt')
            if not prompt:
                return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Initialize OpenAI client
            openai_api_key = settings.OPENAI_API_KEY
            if not openai_api_key:
                return Response({'error': 'OpenAI API key not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            client = OpenAI(api_key=openai_api_key)
            
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract the response text from the completion
            response_text = completion.choices[0].message.content

            return Response({'response': response_text})

        except Exception as e:
            print(f"ChatView Error: {str(e)}")  # Log the error
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
