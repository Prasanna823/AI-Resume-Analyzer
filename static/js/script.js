document.addEventListener("DOMContentLoaded", function () {


    // ---------------------------------------
    // MOBILE / DROPDOWN MENU
    // ---------------------------------------

    const menuButton =
        document.querySelector(".menu-button");

    const dropdown =
        document.querySelector(".dropdown-menu");


    if (menuButton && dropdown) {

        menuButton.addEventListener(
            "click",
            function (event) {

                event.stopPropagation();

                dropdown.classList.toggle("show");

            }
        );


        document.addEventListener(
            "click",
            function () {

                dropdown.classList.remove("show");

            }
        );

    }


    // ---------------------------------------
    // FILE UPLOAD
    // ---------------------------------------

    const fileInput =
        document.getElementById("resumeInput");

    const dropZone =
        document.getElementById("dropZone");

    const fileName =
        document.getElementById("fileName");


    function showFile(file) {

        if (!file) {
            return;
        }


        if (
            !file.name
                .toLowerCase()
                .endsWith(".pdf")
        ) {

            alert("Please upload a PDF file.");

            if (fileInput) {
                fileInput.value = "";
            }

            return;
        }


        if (file.size > 5 * 1024 * 1024) {

            alert(
                "File is too large. Maximum size is 5 MB."
            );

            if (fileInput) {
                fileInput.value = "";
            }

            return;
        }


        if (fileName) {

            fileName.innerHTML = `
                <i class="fa-solid fa-circle-check"></i>
                ${file.name}
            `;

        }

    }


    if (fileInput) {

        fileInput.addEventListener(
            "change",
            function () {

                showFile(this.files[0]);

            }
        );

    }


    // ---------------------------------------
    // DRAG AND DROP
    // ---------------------------------------

    if (dropZone) {

        dropZone.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();

                dropZone.classList.add(
                    "drag-active"
                );

            }
        );


        dropZone.addEventListener(
            "dragleave",
            function () {

                dropZone.classList.remove(
                    "drag-active"
                );

            }
        );


        dropZone.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();

                dropZone.classList.remove(
                    "drag-active"
                );


                const files =
                    event.dataTransfer.files;


                if (
                    files.length > 0 &&
                    fileInput
                ) {

                    fileInput.files = files;

                    showFile(files[0]);

                }

            }
        );

    }


    // ---------------------------------------
    // SCAN BUTTON
    // ---------------------------------------

    const resumeForm =
        document.getElementById("resumeForm");

    const scanButton =
        document.getElementById("scanButton");


    if (resumeForm && scanButton) {

        resumeForm.addEventListener(
            "submit",
            function () {

                scanButton.innerHTML = `
                    <i class="fa-solid fa-spinner fa-spin"></i>
                    Analyzing Resume...
                `;

                scanButton.disabled = true;

            }
        );

    }


    // ---------------------------------------
    // ANIMATED ATS SCORE
    // ---------------------------------------

    const scoreElement =
        document.querySelector(".animated-score");


    if (scoreElement) {

        const target =
            parseInt(
                scoreElement.dataset.score
            ) || 0;


        const number =
            scoreElement.querySelector("span");


        let current = 0;


        const interval =
            setInterval(
                function () {

                    current++;

                    number.textContent =
                        current;


                    if (current >= target) {

                        clearInterval(interval);

                    }

                },
                20
            );

    }


    // ---------------------------------------
    // ANIMATED MATCH %
    // ---------------------------------------

    const matchElement =
        document.querySelector(".match-value");


    if (matchElement) {

        const target =
            parseInt(
                matchElement.dataset.match
            ) || 0;


        let current = 0;


        const interval =
            setInterval(
                function () {

                    current++;

                    matchElement.textContent =
                        current;


                    if (current >= target) {

                        clearInterval(interval);

                    }

                },
                20
            );

    }


    // ---------------------------------------
    // PROGRESS BAR
    // ---------------------------------------

    const progress =
        document.querySelector(".progress-fill");


    if (progress) {

        const value =
            progress.dataset.progress || 0;


        setTimeout(
            function () {

                progress.style.width =
                    value + "%";

            },
            300
        );

    }


});
// ========================================
// SETTINGS
// ========================================

function openSettings(event) {

    if (event) {
        event.preventDefault();
    }

    const overlay =
        document.getElementById("settingsOverlay");

    if (overlay) {

        overlay.classList.add("show");

    }

}


function closeSettings() {

    const overlay =
        document.getElementById("settingsOverlay");

    if (overlay) {

        overlay.classList.remove("show");

    }

}


// Close settings when clicking outside

const settingsOverlay =
    document.getElementById("settingsOverlay");


if (settingsOverlay) {

    settingsOverlay.addEventListener(
        "click",
        function(event) {

            if (event.target === settingsOverlay) {

                closeSettings();

            }

        }
    );

}


// ========================================
// DARK MODE
// ========================================

const darkModeToggle =
    document.getElementById("darkModeToggle");


if (darkModeToggle) {

    const savedMode =
        localStorage.getItem("resumeAI_darkMode");

    if (savedMode === "true") {

        document.body.classList.add("dark-mode");

        darkModeToggle.checked = true;

    }


    darkModeToggle.addEventListener(
        "change",
        function() {

            if (this.checked) {

                document.body.classList.add(
                    "dark-mode"
                );

                localStorage.setItem(
                    "resumeAI_darkMode",
                    "true"
                );

            } else {

                document.body.classList.remove(
                    "dark-mode"
                );

                localStorage.setItem(
                    "resumeAI_darkMode",
                    "false"
                );

            }

        }
    );

}