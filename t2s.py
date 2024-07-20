# from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
# from datasets import load_dataset
# import torch
# import soundfile as sf
# from datasets import load_dataset

# processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
# model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
# vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# inputs = processor(text="PES University, known for its strong emphasis on academic excellence and industry partnerships, boasts impressive college placements with top companies like Microsoft, Google, and Amazon recruiting a significant number of students each year, offering lucrative salary packages and diverse career opportunities.", return_tensors="pt")

# # load xvector containing speaker's voice characteristics from a dataset
# embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
# speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

# speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

# sf.write("speech.wav", speech.numpy(), samplerate=16000)



# import torch
# from parler_tts import ParlerTTSForConditionalGeneration
# from transformers import AutoTokenizer
# import soundfile as sf

# device = "cuda:0" if torch.cuda.is_available() else "cpu"

# model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler_tts_mini_v0.1").to(device)
# tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

# prompt = "PES University, known for its strong emphasis on academic excellence and industry partnerships, boasts impressive college placements with top companies like Microsoft, Google, and Amazon recruiting a significant number of students each year, offering lucrative salary packages and diverse career opportunities."
# description = "A female speaker with a slightly low-pitched voice delivers her words quite expressively, in a very confined sounding environment with clear audio quality. She speaks very fast."

# input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
# prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

# generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
# audio_arr = generation.cpu().numpy().squeeze()
# sf.write("parler_tts_out.wav", audio_arr, model.config.sampling_rate)


from transformers import pipeline
import scipy

synthesiser = pipeline("text-to-speech", "suno/bark-small")

speech = synthesiser("Hello, my dog is cooler than you!", forward_params={"do_sample": True})

scipy.io.wavfile.write("bark_out.wav", rate=speech["sampling_rate"], data=speech["audio"])
