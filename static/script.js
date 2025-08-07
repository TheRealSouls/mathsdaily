document.addEventListener('DOMContentLoaded', () => {
    const symbols = ['∫', '∑', '∆', 'π', '∞', '√', '∂', 'α', 'β', 'γ', '±', '≠', '≤', '≥'];
    const container = document.getElementById("mathSymbols");

    const createMathSymbols = () => {
        setInterval(() => {
            const symbol = document.createElement('div');
            symbol.className = 'math-symbol';
            symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
            symbol.style.left = 10 + Math.random() * 80 + "%";
            symbol.style.animationDuration = (Math.random() * 10 + 15) + 's';
            container.appendChild(symbol);

            setTimeout(() => {
                if (symbol.parentNode) {
                    symbol.parentNode.removeChild(symbol);
                }
            }, 25000);
        }, 2000);
    };

    // 🟢 This is the missing piece
    createMathSymbols();
});