async function saveSettings() {
    const language = document.getElementById("languageSelect").value;
    const voiceMode = document.getElementById("voiceMode").value;
    const voiceEnabled = document.getElementById("voiceEnabled").checked;

    await fetch("/settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language, voice_mode: voiceMode, voice_enabled: voiceEnabled })
    });

    alert("Settings applied successfully.");
}

async function testVoice() {
    const language = document.getElementById("languageSelect").value;
    const voiceMode = document.getElementById("voiceMode").value;

    const response = await fetch("/test_voice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ language, voice_mode: voiceMode })
    });

    const data = await response.json();
    document.getElementById("translatedInstruction").innerText = data.spoken;
}

async function refreshStatus() {
    try {
        const response = await fetch("/status");
        const data = await response.json();

        document.getElementById("instruction").innerText = data.instruction || "System ready.";
        document.getElementById("translatedInstruction").innerText = data.translated_instruction || "System ready.";

        const pill = document.getElementById("dangerPill");
        pill.className = "status-pill";
        if (data.danger_level === "medium") pill.classList.add("medium");
        if (data.danger_level === "high") pill.classList.add("high");
        pill.innerText = (data.danger_level || "safe").toUpperCase();

        const list = document.getElementById("objectsList");
        list.innerHTML = "";

        if (!data.detections || data.detections.length === 0) {
            list.innerHTML = "<li>No objects detected.</li>";
            return;
        }

        data.detections.forEach(obj => {
            const li = document.createElement("li");
            li.innerText = `${obj.label} — confidence ${obj.confidence}`;
            list.appendChild(li);
        });
    } catch (error) {
        console.log(error);
    }
}

setInterval(refreshStatus, 1200);
