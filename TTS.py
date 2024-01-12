import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = ""
service_region = "westeurope"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
speech_config.speech_synthesis_voice_name = "az-AZ-BanuNeural"

def talk(text):
  ssml = f'<speak version=\'1.0\' xml:lang=\'en-US\'><voice name=\'az-AZ-BanuNeural\'><prosody rate=\'fast\'>{text}</prosody></voice></speak>'
  # use the default speaker as audio output.
  speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
  result = speech_synthesizer.speak_ssml_async(ssml).get()
  # Check result
  if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
      print(f"Speech synthesized for text [{text}]")
  elif result.reason == speechsdk.ResultReason.Canceled:
      cancellation_details = result.cancellation_details
      print(f"Speech synthesis canceled: {cancellation_details.reson}")
      if cancellation_details.reason == speechsdk.CancellationReason.Error:
          print(f"Error details: {cancellation_details.error_details}")

if __name__ == "__main__":
    talk()