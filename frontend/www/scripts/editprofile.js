async function updateBio() {
    let form = document.querySelector("#updateUserBio");
    let formData = new FormData(form);
    let body = {
        "bio": formData.get("bio")
    };

    let user = await getCurrentUser();

    let response = await sendRequest("PUT", `${HOST}/api/users/updateBio/${user.id}/`, body);
    if (response.ok) {
        window.location.replace("profile.html");
    }
}

document.querySelector("#save-btn").addEventListener("click", async () => await updateBio() );