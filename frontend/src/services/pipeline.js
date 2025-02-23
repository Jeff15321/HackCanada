const BASE_URL = 'https://72ddc6f7069330b4c304c2f4e662bd321785dd91-3000.dstack-prod5.phala.network';

async function runPipeline() {
  try {

    console.log('Calling /api/nft/mint...');
    const mintPayload = {
      token_id: "plant-tee-10894",
      receiver_id: "hackcanada.testnet",
      plant_metadata: {
        glb_file_url: "https://example.com/plant.glb",
        parameters: {
          color_vibrancy: { score: 95, explanation: "Vibrant green" },
          leaf_area_index: { score: 85, explanation: "Good coverage" },
          wilting: { score: 90, explanation: "No wilting" },
          spotting: { score: 100, explanation: "No spots" },
          symmetry: { score: 88, explanation: "Good symmetry" }
        },
        name: "TEE Plant #3",
        wallet_id: "hackcanada.testnet",
        price: "1000000000000000000000000"
      }
    };
    response = await fetch(`${BASE_URL}/api/nft/mint`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(mintPayload)
    });
    result = await response.json();
    console.log('Mint NFT result:', result);

    // 4. Get NFT Metadata
    console.log('Calling /api/nft/metadata/plant-tee-14...');
    response = await fetch(`${BASE_URL}/api/nft/metadata/plant-tee-14`);
    result = await response.json();
    console.log('NFT Metadata:', result);

    // 5. Get NFT Token Details
    console.log('Calling /api/nft/token/plant-tee-13...');
    response = await fetch(`${BASE_URL}/api/nft/token/plant-tee-14`);
    result = await response.json();
    console.log('NFT Token Details:', result);

    // 6. Get Tokens for an Owner (Original Owner: hackcanada.testnet)



    response = await fetch(`${BASE_URL}/api/nft/tokens/hackcanada.testnet`);
    result = await response.json();
    console.log('Tokens for hackcanada.testnet:', result);

  } catch (error) {
    console.error('Pipeline error:', error);
  }
}

runPipeline();