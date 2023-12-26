const items = document.getElementsByClassName('like-section')
function getCSRFToken() {
    // Extract the CSRF token from the cookie
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

    return cookieValue;
}

const csrfToken = getCSRFToken();

for (let item of items) {
    const [buttonLike, buttonDislike, text, counter] = item.children;
    buttonLike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', buttonLike.dataset.id);

        const request = new Request('question_like', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count + 1;
            });
    });
    buttonDislike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', buttonLike.dataset.id);

        const request = new Request('question_like', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                counter.innerHTML = data.count - 1;
            });
    });

}