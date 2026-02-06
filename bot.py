<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>DINO 76 🍣</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>

  <style>
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 15px;
      background: url('https://images.unsplash.com/photo-1553621042-f6e147245754?auto=format&fit=crop&w=1050&q=80') no-repeat center center fixed;
      background-size: cover;
      color: #ffffff;
    }

    h1 {
      text-align: center;
      text-shadow: 1px 1px 4px #000;
      margin-bottom: 20px;
    }

    .products {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
    }

    .product, .detail {
      background: rgba(0,0,0,0.7);
      border-radius: 12px;
      padding: 15px;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
      backdrop-filter: blur(5px);
    }

    button {
      margin-top: 10px;
      padding: 12px;
      width: 100%;
      border: none;
      border-radius: 10px;
      background: #ff6347;
      color: white;
      font-size: 16px;
      cursor: pointer;
    }

    .back {
      background: #444;
    }

    .price {
      color: #00ff9c;
      font-weight: bold;
    }

    video {
      width: 100%;
      border-radius: 12px;
      margin-bottom: 12px;
    }
  </style>
</head>

<body>

<h1>🦖🍣 DINO 76 Sushi</h1>

<!-- ACCUEIL -->
<div id="home">
  <div class="products">
    <div class="product">
      <h3>🥶 FROZEN SIFT</h3>
      <button onclick="openProduct('frozen')">Voir</button>
    </div>

    <div class="product">
      <h3>🍤 Sushi Nigiri</h3>
      <button onclick="openProduct('nigiri')">Voir</button>
    </div>
  </div>
</div>

<!-- DÉTAIL -->
<div id="productDetail" style="display:none;"></div>

<script>
const contact = "@DINOS76S";

const products = {
  frozen: {
    name: "FROZEN SIFT 🥶",
    video: "caliplates.mp4",
    description: `🧑‍⚕️
- Garlic coockie 🍪🍪✅
- JELLY DONUTS 🍩 🌈✅
- 🍰 ✅

Nous sommes sur une gamme très solide et une farm réputée pour ses TERPS gourmands. Le meilleur du Frozen !
🍑🍓🍋🥭🍊

Promotion 25% pour ouverture la famille !!!`,
    prices: [
      "2,5G : 50€",
      "5G : 90€",
      "10G : 180€",
      "20G : 350€",
      "25G : 400€"
    ]
  },
  nigiri: {
    name: "Sushi Nigiri 🍤",
    description: "Sushi Nigiri premium avec poisson frais sur lit de riz vinaigré. Une explosion de saveurs !",
    prices: [
      "2 pièces : 6€",
      "5 pièces : 14€",
      "10 pièces : 26€"
    ]
  }
};

function openProduct(key) {
  const p = products[key];

  let html = `<div class="detail">`;

  // Ajouter la vidéo si elle existe
  if(p.video) {
    html += `<video src="${p.video}" controls></video>`;
  }

  html += `
      <h2>${p.name}</h2>
      <p>${p.description}</p>
      <h4>💰 Tarifs</h4>
  `;

  p.prices.forEach(price => {
    html += `<p class="price">${price}</p>`;
  });

  const message = encodeURIComponent(
    `Bonjour, je souhaite commander : ${p.name}`
  );

  html += `
      <button onclick="order('${message}')">📩 Commander</button>
      <button class="back" onclick="goBack()">⬅ Retour</button>
    </div>
  `;

  document.getElementById("home").style.display = "none";
  const detail = document.getElementById("productDetail");
  detail.innerHTML = html;
  detail.style.display = "block";
}

function goBack() {
  document.getElementById("productDetail").style.display = "none";
  document.getElementById("home").style.display = "block";
}

function order(message) {
  window.open(`https://t.me/${contact.replace("@","")}?text=${message}`, "_blank");
}
</script>

</body>
</html>
