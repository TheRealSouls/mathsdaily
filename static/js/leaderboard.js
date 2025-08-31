async function loadLeaderboard(limit) {
    const res = await fetch(`/api/leaderboard?limit=${limit}`)
    const data = await res.json();

    const container = document.getElementById("table-content");
    container.innerHTML = "";

    data.forEach((player, index) => {
        const row = document.createElement("div");
        row.classList.add("leaderboard-row");

        row.innerHTML = `
            <h3 class="rank-number">${index + 1}</h3>
            <h3 class="user-name">${player.username}</h3>
            <div class="user-stats">
                <p class="user-xp">
                    <span>${player.score}</span>
                    Points
                </p>
                <p class="user-solved">
                    <span>${player.solved ?? 0}</span>
                    Solved
                </p>
                <p class="user-accuracy">
                    <span>${((player.accuracy ?? 0) * 100).toFixed(2)}%</span>
                    Accuracy
                </p>
            </div>
        `;

        container.appendChild(row);
    })
}

document.querySelectorAll("#limit-buttons button").forEach(btn => {
    btn.addEventListener("click", () => {
        const limit = btn.innerText.split(" ")[1];
        loadLeaderboard(limit);
    })
})

document.addEventListener("DOMContentLoaded", () => loadLeaderboard(10));