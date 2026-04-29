<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Will Tech Solutions</title>
    <style>
        body { background-color: #0a0e12; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 10px; }
        .header { text-align: center; color: #4fd1ed; font-size: 24px; margin-bottom: 15px; text-shadow: 0 0 10px #4fd1ed66; font-weight: bold; }
        .ticker-bar { display: flex; justify-content: space-around; font-size: 12px; border-bottom: 1px solid #1a222d; padding-bottom: 10px; }
        .gold-txt { color: #ffd700; } .up { color: #00ff88; } .down { color: #ff4444; }
        
        .main-chart { background: #111820; border-radius: 10px; padding: 15px; margin-top: 15px; border: 1px solid #1a222d; }
        .prediction-badge { background: #00ff8822; color: #00ff88; padding: 5px 10px; border-radius: 5px; float: right; font-weight: bold; }
        
        .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
        .card { background: #161d26; padding: 15px; border-radius: 10px; border: 1px solid #1a222d; }
        
        .auto-button {
            background: none; border: 2px solid #00ff88; color: #00ff88; border-radius: 10px;
            padding: 15px 5px; text-align: center; font-weight: bold; box-shadow: 0 0 15px #00ff8833;
            cursor: pointer; transition: 0.3s;
        }
        .active-trade { background: #00ff88 !important; color: #000 !important; box-shadow: 0 0 25px #00ff88 !important; }
        .footer-status { color: #00ff88; font-size: 11px; text-align: center; margin-top: 20px; text-transform: uppercase; }
    </style>
</head>
<body>

    <div class="header">Will Tech Solutions</div>

    <div class="ticker-bar">
        <span>GOLD: <span id="top-gold-price" class="gold-txt">---</span> <span id="top-gold-var">---</span></span>
        <span>BTC/USDT: <span id="top-btc-price" class="up">---</span> <span id="top-btc-var">---</span></span>
    </div>

    <div class="main-chart">
        <div><strong>BITCOIN (BTC)</strong> <span id="ia-prediction" class="prediction-badge">IA: ANALISANDO...</span></div>
        <div style="font-size: 22px; margin: 10px 0;"><span id="main-btc-price">$0.00</span> 
            <small id="main-btc-var" class="down" style="font-size: 12px;">0.00%</small>
        </div>
        <div id="chart" style="height: 100px; background: #0d1218; border-radius: 5px; border: 1px dashed #333; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #444;">
            [LGBM MODEL ACTIVE MONITORING]
        </div>
    </div>

    <div class="grid-container">
        <div class="card">
            <small>SOLANA (SOL)</small><br>
            <span id="sol-data" class="up">---</span>
        </div>
        <div class="card">
            <small>GOLD (PAXG)</small><br>
            <span id="gold-data" class="gold-txt">---</span>
        </div>
    </div>

    <h4 style="margin-bottom: 10px; font-size: 14px;">AUTOTRADE AUTOMATION</h4>
    <div class="grid-container" style="grid-template-columns: 1fr 1fr 1fr;">
        <div id="btn-smc" class="auto-button">AUTO<br><small>SMC</small></div>
        <div id="btn-ob" class="auto-button">AUTO<br><small>ORDER BLOCK</small></div>
        <div id="btn-trend" class="auto-button">AUTO<br><small>TREND</small></div>
    </div>

    <div id="status-msg" class="footer-status">SISTEMA INICIALIZANDO...</div>

    <script>
        async function buscarDados() {
            try {
                const response = await fetch('http://127.0.0.1:5000/dados');
                const dados = await response.json();

                // Atualiza BITCOIN
                const btc = dados["BTCUSDT"];
                document.getElementById('top-btc-price').innerText = `$${btc.preco.toLocaleString()}`;
                document.getElementById('main-btc-price').innerText = `$${btc.preco.toLocaleString()}`;
                document.getElementById('top-btc-var').innerText = `${btc.variacao}%`;
                document.getElementById('ia-prediction').innerText = `IA: ${btc.prob}%`;
                
                // Atualiza SOLANA
                const sol = dados["SOLUSDT"];
                document.getElementById('sol-data').innerText = `$${sol.preco} (${sol.variacao}%)`;

                // Atualiza GOLD
                const gold = dados["PAXGUSDT"];
                document.getElementById('top-gold-price').innerText = `$${gold.preco}`;
                document.getElementById('gold-data').innerText = `$${gold.preco} (${gold.variacao}%)`;

                // Lógica de Automação Visual (Ativa botões se a probabilidade for alta)
                if (btc.prob > 80) {
                    document.getElementById('btn-smc').classList.add('active-trade');
                    document.getElementById('status-msg').innerText = `SINAL DE ALTA DETECTADO: BTC @ $${btc.preco}`;
                } else {
                    document.getElementById('btn-smc').classList.remove('active-trade');
                }

            } catch (e) {
                console.log("Erro: O servidor Python está desligado.");
                document.getElementById('status-msg').innerText = "OFFLINE: LIGUE O BACKEND PYTHON";
            }
        }
        setInterval(buscarDados, 2000); // Atualiza a cada 2 segundos
    </script>
</body>
</html>
