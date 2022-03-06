async function fetchProfile() {
    let user = await getCurrentUser();

    let nameSpan = document.querySelector(".name");
    nameSpan.innerHTML = user.username;

    let dateJoinedSpan = document.querySelector(".join");
    let dateJoined = new Date(user.date_joined);
    dateJoinedSpan.innerHTML = dateJoined.toString();

    let textSpan = document.querySelector(".text");
    if (user.bio) {
        textSpan.innerHTML = user.bio;
    } else {
        textSpan.innerHTML = "Your bio is empty. Edit your profile to add some words about yourself!";
    }
}

window.addEventListener("DOMContentLoaded", async () => {
    await fetchProfile();
});