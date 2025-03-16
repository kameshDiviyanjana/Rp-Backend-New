let model;
const loadModel = async () => {
  const modelPath = `file://${path.resolve(
    __dirname,
    "tfjs_model/model.json"
  )}`;
  model = await tf.loadLayersModel(modelPath);
  console.log("Model loaded successfully!");
};

// Preprocess the audio file and generate MFCCs
export async function preprocessAudio(filePath) {
  const y = await librosa.load(filePath, { sr: 16000 }); // Load at 16kHz
  const mfccs = librosa.feature.mfcc(y, { sr: 16000, n_mfcc: 13 });
  const paddedMfccs = tf.pad(
    tf.tensor(mfccs),
    [
      [0, Math.max(0, 100 - mfccs.shape[0])],
      [0, 0],
    ], // Pad timesteps to 100
    "constant"
  );
  return paddedMfccs.expandDims(0); // Add batch dimension
}
