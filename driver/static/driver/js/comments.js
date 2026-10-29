document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.toggle-button');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const sectionId = this.getAttribute('data-section-id');
            const commentSection = document.getElementById('comment-section-' + sectionId);

            // Переключаем видимость блока комментариев
            commentSection.classList.toggle('hidden');
            commentSection.classList.toggle('visible');
        });
    });
});
