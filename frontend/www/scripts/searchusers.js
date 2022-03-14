async function searchUsers() {
    console.log("search users");
    let searchString = sessionStorage.getItem("searchString");
    if (searchString != null) {
        document.querySelector("#search-keyword").innerHTML = `Searching for ${searchString}...`;

        let response = await sendRequest("GET", `${HOST}/api/users/searchUsername/${searchString}/`);
        if (response.ok) {
            let data = await response.json();
            let listUsers = document.querySelector(".list-users");
            for (let i of data) {
                console.log(i);
                listUsers.innerHTML += `
                    <div class="nearby-user">
                        <div class="row">
                          <div class="col-md-2 col-sm-2">
                            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="user" class="profile-photo-lg">
                          </div>
                          <div class="col-md-7 col-sm-7">
                            <h5><a href="#" class="profile-link">${i.username}</a></h5>
                          </div>
                          <div class="col-md-3 col-sm-3">
                            <button class="btn btn-primary pull-right">Add Friend</button>
                          </div>
                        </div>
                    </div>
                `;
            }
        }
    }
}

window.addEventListener("load", async () => { await searchUsers(); });