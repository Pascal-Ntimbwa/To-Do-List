










function likeUnlike(postId) {
    const likeButton = document.getElementById(`likeButton_${postId}`);
    
    fetch(`/like_unlike/${postId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            likeButton.innerText = data.liked ? "Unlike" : "Like";
            updateLikeCount(postId, data.like_count);
        } else {
            console.error(data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}


function updateLikeCount(postId, likeCount) {
    const likeCountElement = document.getElementById(`likeCount_${postId}`);
    likeCountElement.innerText = likeCount;
}


