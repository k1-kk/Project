const loadBtn = document.getElementById("loadBtn");
const movieGrid = document.getElementById("movieGrid");
const statusText = document.getElementById("status");
const minRatingInput = document.getElementById("min-rating");
const maxRatingInput = document.getElementById("max-rating");
const limitInput = document.getElementById("limit");

loadBtn.addEventListener("click",async() =>{
    statusText.textContent = "加载中...";
    movieGrid.innerHTML = "";

    try {
        const minRating = minRatingInput.value || 0;
        const maxRating = maxRatingInput.value || 10;
        const limit = limitInput.value || 20;
        const url = `http://127.0.0.1:8000/movies?min_rating=${minRating}&max_rating=${maxRating}&limit=${limit}`;

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("接口请求失败");
        }

        const movies = await response.json();
                
        movies.forEach(movie => {
            const card = document.createElement("div");
            card.className = "movie-card";

            const imageUrl = `http://127.0.0.1:8000/proxy-image?url=${encodeURIComponent(movie.cover_url)}`;

            card.innerHTML = `
                <img src="${imageUrl}" alt="${movie.title} 封面" class="movie-cover">
                <h3>${movie.title}</h3>
                <p>评分：${movie.rating}</p>
            `;

            movieGrid.appendChild(card);
        });

        if (movies.length === 0) {
            statusText.textContent = "没有找到符合条件的电影";
            return;
        }

        statusText.textContent = `加载完成，共${movies.length}部电影`;
    }catch(error){
        statusText.textContent = `加载失败，请检查后端程序是否启动`;
    };
});
