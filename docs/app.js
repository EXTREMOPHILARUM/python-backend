let currentIndex = 1;
const totalFiles = 12;  

function fetchAndDisplayMarkdown(index) {
    fetch(`docs/${index}.md`)
        .then(response => response.text())
        .then(md => {
            document.getElementById('content').innerHTML = marked(md);
            updateNavigationButtons();
        });
}

function updateNavigationButtons() {
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
    
    prevButton.disabled = currentIndex <= 1;
    nextButton.disabled = currentIndex >= totalFiles;

    prevButton.addEventListener('click', () => {
        if (currentIndex > 1) {
            currentIndex--;
            fetchAndDisplayMarkdown(currentIndex);
        }
    });

    nextButton.addEventListener('click', () => {
        if (currentIndex < totalFiles) {
            currentIndex++;
            fetchAndDisplayMarkdown(currentIndex);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchAndDisplayMarkdown(currentIndex);
});
