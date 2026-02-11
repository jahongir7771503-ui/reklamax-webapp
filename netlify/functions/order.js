const fetch = require("node-fetch");

exports.handler = async function (event, context) {

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      body: "Method Not Allowed"
    };
  }

  const data = JSON.parse(event.body);

  const BOT_TOKEN = "SENING_BOT_TOKENING";
  const CHAT_ID = "SENING_CHAT_IDING";

  const message = `
🆕 WebApp Buyurtma

📞 Telefon: ${data.phone}
📐 O'lcham: ${data.size}
📍 Joy: ${data.place}
🎨 Uslub: ${data.style}
🌈 Rang: ${data.color}
`;

  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: CHAT_ID,
      text: message
    })
  });

  return {
    statusCode: 200,
    body: JSON.stringify({ status: "ok" })
  };
};
