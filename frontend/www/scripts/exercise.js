let cancelButton;
let okButton;
let deleteButton;
let editButton;
let oldFormData;

class MuscleGroup { 
    constructor(type) {
        this.isValidType = false;
        this.validTypes = ["Legs", "Chest", "Back", "Arms", "Abdomen", "Shoulders"]

        this.type = this.validTypes.includes(type) ? type : undefined;
    };

    setMuscleGroupType = (newType) => {
        this.isValidType = false;
        
        if(this.validTypes.includes(newType)){
            this.isValidType = true;
            this.type = newType;
        }
        else{
            alert("Invalid muscle group!");
        }

    };
    
    getMuscleGroupType = () => {
        console.log(this.type, "SWIOEFIWEUFH")
        return this.type;
    }
}

function handleCancelButtonDuringEdit() {
    setReadOnly(true, "#form-exercise");
    document.querySelector("select").setAttribute("disabled", "")
    okButton.className += " hide";
    deleteButton.className += " hide";
    cancelButton.className += " hide";
    editButton.className = editButton.className.replace(" hide", "");

    // updateDisplay(oldFormData);
    toggleVisibility();

    cancelButton.removeEventListener("click", handleCancelButtonDuringEdit);

    let form = document.querySelector("#form-exercise");
    if (oldFormData.has("name")) form.name.value = oldFormData.get("name");
    if (oldFormData.has("description")) form.description.value = oldFormData.get("description");
    if (oldFormData.has("instructions")) form.instructions.value = oldFormData.get("instructions");
    if (oldFormData.has("duration")) form.duration.value = oldFormData.get("duration");
    if (oldFormData.has("calories")) form.calories.value = oldFormData.get("calories");
    if (oldFormData.has("muscleGroup")) form.muscleGroup.value = oldFormData.get("muscleGroup");
    if (oldFormData.has("unit")) form.unit.value = oldFormData.get("unit");
    if (oldFormData.has("video")) form.video.value = oldFormData.get("video");
    
    oldFormData.delete("name");
    oldFormData.delete("description");
    oldFormData.delete("instructions");
    oldFormData.delete("duration");
    oldFormData.delete("calories");
    oldFormData.delete("muscleGroup");
    oldFormData.delete("unit");
    oldFormData.delete("video");

}

function handleCancelButtonDuringCreate() {
    window.location.replace("exercises.html");
}

async function createExercise() {
    document.querySelector("select").removeAttribute("disabled")
    let form = document.querySelector("#form-exercise");
    let formData = new FormData(form);

    let user = await getCurrentUser();

    let videoURL = processYoutubeURL(formData.get("video"));
    formData.set("video", videoURL);

    let body = {"name": formData.get("name"), 
                "description": formData.get("description"),
                "instructions": formData.get("instructions"),
                "duration": formData.get("duration"),
                "calories": formData.get("calories"),
                "muscleGroup": formData.get("muscleGroup"), 
                "unit": formData.get("unit"), 
                "video": formData.get("video"),
                "owner": user["url"],
                "owner_name": user["username"]
            };

    let response = await sendRequest("POST", `${HOST}/api/exercises/`, body);

    if (response.ok) {
        window.location.replace("exercises.html");
    } else {
        let data = await response.json();
        let alert = createAlert("Could not create new exercise!", data);
        document.body.prepend(alert);
    }
}

function handleEditExerciseButtonClick() {
    setReadOnly(false, "#form-exercise");

    document.querySelector("select").removeAttribute("disabled")

    editButton.className += " hide";
    okButton.className = okButton.className.replace(" hide", "");
    cancelButton.className = cancelButton.className.replace(" hide", "");
    deleteButton.className = deleteButton.className.replace(" hide", "");


    toggleVisibility();

    cancelButton.addEventListener("click", handleCancelButtonDuringEdit);

    let form = document.querySelector("#form-exercise");
    oldFormData = new FormData(form);
}

async function deleteExercise(id) {
    let response = await sendRequest("DELETE", `${HOST}/api/exercises/${id}/`);
    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert(`Could not delete exercise ${id}`, data);
        document.body.prepend(alert);
    } else {
        window.location.replace("exercises.html");
    }
}

function updateDisplay(response) {
    for (let key of Object.keys(response)) {
        let ele = document.querySelector(`#${key}`)
        if (ele != null) {
            ele.textContent = response[key];
        }
    }

    toggleVisibility();

    let player = document.querySelector("#youtube-player");

    if (player.src != response["video"]) {
        player.src = response["video"];
    }

    if (player.src == "") {
        player.classList.replace("visible", "hidden");
    }
}

async function retrieveExercise(id) {
    let response = await sendRequest("GET", `${HOST}/api/exercises/${id}/`);
    // let currentUserResponse = await sendRequest("GET", `${HOST}/api/currentUser/`);
    console.log(response.ok)

    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert("Could not retrieve exercise data!", data);
        document.body.prepend(alert);
    } else {
        document.querySelector("select").removeAttribute("disabled")
        let exerciseData = await response.json();
        // let userData = await currentUserResponse.json();    
        let userData = await getCurrentUser();

        let form = document.querySelector("#form-exercise");
        let formData = new FormData(form);

        for (let key of formData.keys()) {
            let selector
            key !== "muscleGroup" ? selector = `input[name="${key}"], textarea[name="${key}"]` : selector = `select[name=${key}]`;
            let input = form.querySelector(selector);
            let newVal = exerciseData[key];
            input.value = newVal;
        }
        document.querySelector("select").setAttribute("disabled", "");
        document.querySelector("#owner-name").textContent = exerciseData["owner_name"];

        if (exerciseData["owner"] != userData["url"]) {
            editButton.classList  += " hide";
        }

        updateDisplay(exerciseData);

    }
}

function toggleVisibility() {
    let visible = document.querySelectorAll(".visible");
    let hidden = document.querySelectorAll(".hidden");

    visible.forEach(x => {
        x.classList.replace("visible", "hidden");
    });

    hidden.forEach(x => {
        x.classList.replace("hidden", "visible");
    })
}

function processYoutubeURL(url) {
    let domain = "youtu.be";
    let embedDomain = "https://www.youtube.com/embed/";
    let timeTag = "?t=";
    let srcAtt = "src=\"";
    let newURL;
    let idx;

    idx = url.search(srcAtt);
    // Implies that the embed html is provided instead of just the URL
    if (idx > -1) {
        let newIdx = srcAtt.length + idx;
        let htmlCodeSubstr = url.substring(newIdx);

        idx = htmlCodeSubstr.search("\"");
        url = htmlCodeSubstr.substring(0, idx);
    }

    idx = url.search(domain);
    if (idx > -1) {
        let newIdx = domain.length + idx + 1;
        let appendix = url.substring(newIdx);
        newURL = `${embedDomain}${appendix}`;
    } else {
        newURL = url.replace("watch?v=", "embed/");
    }

    newURL = newURL.replace(timeTag, "?start=");

    return newURL;
}

async function updateExercise(id) {
    let form = document.querySelector("#form-exercise");
    let formData = new FormData(form);

    let muscleGroupSelector = document.querySelector("select")
    muscleGroupSelector.removeAttribute("disabled")

    let selectedMuscleGroup = new MuscleGroup(formData.get("muscleGroup"));

    let videoURL = formData.get("video");
    videoURL = processYoutubeURL(videoURL);
    formData.set("video", videoURL);
    document.querySelector("#inputVideoURL").value = videoURL;

    let body = {"name": formData.get("name"), 
                "description": formData.get("description"),
                "instructions": formData.get("instructions"),
                "duration": formData.get("duration"),
                "calories": formData.get("calories"),
                "muscleGroup": selectedMuscleGroup.getMuscleGroupType(),
                "unit": formData.get("unit"), 
                "video": formData.get("video")
            };
    let response = await sendRequest("PUT", `${HOST}/api/exercises/${id}/`, body);

    if (!response.ok) {
        let data = await response.json();
        let alert = createAlert(`Could not update exercise ${id}`, data);
        document.body.prepend(alert);
    } else {
        muscleGroupSelector.setAttribute("disabled", "")
        // duplicate code from handleCancelButtonDuringEdit
        // you should refactor this
        setReadOnly(true, "#form-exercise");
        okButton.className += " hide";
        deleteButton.className += " hide";
        cancelButton.className += " hide";
        editButton.className = editButton.className.replace(" hide", "");
    
        cancelButton.removeEventListener("click", handleCancelButtonDuringEdit);
        
        

        updateDisplay(body);

        oldFormData.delete("name");
        oldFormData.delete("description");
        oldFormData.delete("instructions");
        oldFormData.delete("duration");
        oldFormData.delete("calories");
        oldFormData.delete("muscleGroup");
        oldFormData.delete("unit");
        oldFormData.delete("video");
    }
}

window.addEventListener("DOMContentLoaded", async () => {
    cancelButton = document.querySelector("#btn-cancel-exercise");
    okButton = document.querySelector("#btn-ok-exercise");
    deleteButton = document.querySelector("#btn-delete-exercise");
    editButton = document.querySelector("#btn-edit-exercise");
    oldFormData = null;

    const urlParams = new URLSearchParams(window.location.search);

    // view/edit
    if (urlParams.has('id')) {
        const exerciseId = urlParams.get('id');
        await retrieveExercise(exerciseId);

        editButton.addEventListener("click", handleEditExerciseButtonClick);
        deleteButton.addEventListener("click", (async (id) => await deleteExercise(id)).bind(undefined, exerciseId));
        okButton.addEventListener("click", (async (id) => await updateExercise(id)).bind(undefined, exerciseId));
    } 
    //create
    else {
        setReadOnly(false, "#form-exercise");

        editButton.className += " hide";
        okButton.className = okButton.className.replace(" hide", "");
        cancelButton.className = cancelButton.className.replace(" hide", "");

        okButton.addEventListener("click", async () => await createExercise());
        cancelButton.addEventListener("click", handleCancelButtonDuringCreate);
    }
});