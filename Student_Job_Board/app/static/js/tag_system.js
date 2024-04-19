document.addEventListener("DOMContentLoaded", function () {
  var addedKeySkills = [];

  function createTagButton(content) {
    var tagButton = document.createElement("button");
    tagButton.classList.add(
      "btn",
      "btn-success",
      "me-2",
      "mb-2",
      "position-relative"
    );
    tagButton.type = "button";
    tagButton.textContent = content + " ";

    var removeButton = document.createElement("button");
    removeButton.classList.add("btn-close");
    removeButton.setAttribute("aria-label", "Remove");

    removeButton.onclick = function () {
      tagButton.remove();
      var index = addedKeySkills.indexOf(content);
      addedKeySkills.splice(index, 1);
      updateHiddenFields();
    };

    tagButton.appendChild(removeButton);
    return tagButton;
  }

  function updateHiddenFields() {
    document.getElementById("skills_input").value = addedKeySkills.join(",");
  }

  function addKeySkill() {
    var newSkill = document
      .getElementById("new_skill_input")
      .value.trim()
      .toLowerCase();
    if (newSkill !== "") {
      var skillContainer = document.getElementById("selectedSkillsContainer");
      if (addedKeySkills.includes(newSkill)) {
        alert("Skill already exists.");
        return;
      }
      if (skillContainer.children.length < 10) {
        var skillButton = createTagButton(newSkill);
        skillContainer.appendChild(skillButton);
        document.getElementById("new_skill_input").value = "";
        addedKeySkills.push(newSkill);
        updateHiddenFields();
      } else {
        alert("Maximum limit of 10 tags reached.");
      }
    }
  }

  document
    .getElementById("addSkillButton")
    .addEventListener("click", addKeySkill);
});
