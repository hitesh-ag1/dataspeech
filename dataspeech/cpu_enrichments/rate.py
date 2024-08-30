from g2p import make_g2p

transducer = make_g2p('eng', 'eng-ipa')

def rate_apply(batch, rank=None, audio_column_name="audio", text_column_name="text"):
    if isinstance(batch[text_column_name], list):  
        speaking_rates1 = []
        speaking_rates2 = []
        phonemes_list = []
        if "speech_duration" in batch:
            for text, audio_duration in zip(batch[text_column_name], batch["speech_duration"]):
                phonemes = transducer(text).output_string
                audio_duration = audio_duration if audio_duration != 0 else 0.01
                speaking_rate1 = len(phonemes) / audio_duration
                speaking_rate2 = len(text) / audio_duration
                speaking_rates1.append(speaking_rate1)
                speaking_rates2.append(speaking_rate2)
                phonemes_list.append(phonemes)
        else:
            for text, audio in zip(batch[text_column_name], batch[audio_column_name]):
                phonemes = transducer(text).output_string
                sample_rate = audio["sampling_rate"]
                audio_length = len(audio["array"].squeeze()) / sample_rate
                
                speaking_rate1 = len(phonemes) / audio_length
                speaking_rate2 = len(text) / audio_length

                
                speaking_rates1.append(speaking_rate1)
                speaking_rates2.append(speaking_rate2)
                phonemes_list.append(phonemes)
        
        batch["speaking_rate_phn"] = speaking_rates1
        batch["speaking_rate_txt"] = speaking_rates2
        batch["phonemes"] = phonemes_list
    else:
        phonemes = transducer(batch[text_column_name]).output_string
        if "speech_duration" in batch:
            audio_length = batch["speech_duration"] if batch["speech_duration"] != 0 else 0.01
        else:
            sample_rate = batch[audio_column_name]["sampling_rate"]
            audio_length = len(batch[audio_column_name]["array"].squeeze()) / sample_rate

        speaking_rate1 = len(phonemes) / audio_length
        speaking_rate2 = len(batch[text_column_name]) / audio_length
        
        batch["speaking_rate_phn"] = speaking_rate1
        batch["speaking_rate_txt"] = speaking_rate2
        batch["phonemes"] = phonemes

    return batch