// Remove member functionality
document.querySelectorAll('.remove-member').forEach(button => {
    button.addEventListener('click', function() {
        if (confirm("Are you sure you want to remove this member?")) {
            const membershipId = this.dataset.membershipId;

            fetch(`/groups/membership/${membershipId}/remove/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('.list-group-item').remove();
                }
            });
        }
    });
});

// Join group functionality
document.querySelector('.join-group')?.addEventListener('click', function() {
    const groupId = this.dataset.groupId;
    this.disabled = true;

    fetch(`/groups/${groupId}/join/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message);
            this.disabled = false;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        this.disabled = false;
    });
});

// Leave group functionality
document.querySelector('.leave-group')?.addEventListener('click', function() {
    if (confirm("'Are you sure you want to leave this group?")) {
        const groupId = this.dataset.groupId;
        this.disabled = true;

        fetch(`/groups/${groupId}/leave/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
                this.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            this.disabled = false;
        });
    }
});

// Delete comment functionality

document.querySelectorAll('.delete-comment').forEach(button => {
    button.addEventListener('click', function() {
        if (confirm("Are you sure you want to delete this comment?")) {
            const commentId = this.dataset.commentId;
            this.disabled = true;

            fetch(`/groups/comments/${commentId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.closest('.mb-4').remove();
                } else {
                    alert(data.message);
                    this.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.disabled = false;
            });
        }
    });
});

function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

