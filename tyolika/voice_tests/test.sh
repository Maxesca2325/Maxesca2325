TEXT="Sispann peye pou flyer ou. Avèk entèlijans atifisyèl, ou ka fè youn ki sanble pwofesyonèl, nan twa minit, sou telefòn ou."
for v in fishaudio_10242bedf1a24be8986de0fc2360c12a fishaudio_28ebfd4401f84942a7f65b4a04ae8aba fishaudio_19b5a40bf5214220b45b101bb4328810 fishaudio_60f8a4295de94954ac6072bfa04195f7 fishaudio_e0e24fe6c80648a0bd01eb4596e4d301; do
  curl -sS -H "xi-api-key: proxy-injected" -X POST https://api.ai33.pro/v3/text-to-speech --form-string "text=$TEXT" --form-string "voice_id=$v" --form-string "speed=1" --form-string "with_transcript=false" | python3 -c "import json,sys; j=json.load(sys.stdin); print('$v', j.get('task_id'), j.get('message',''))"
done
