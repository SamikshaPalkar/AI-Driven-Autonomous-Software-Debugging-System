document.addEventListener("DOMContentLoaded", () => {

    const analyzeBtn = document.getElementById("analyzeBtn");
    const autofixBtn = document.getElementById("autofixBtn");
    const pdfBtn = document.getElementById("pdfBtn");
    const codeInput = document.getElementById("codeInput");
    const output = document.getElementById("output");
    const language = document.getElementById("language");

    analyzeBtn.addEventListener("click", async () => {

        const code = codeInput.value;
        const lang = language.value;

        output.innerHTML = "Analyzing...";

        const formData = new FormData();
        formData.append("code", code);
        formData.append("language", lang);

        const res = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        output.innerHTML = `
            <h3>🔎 Analysis</h3>
            <pre>${JSON.stringify(data.analysis, null, 2)}</pre>

            <h3>📌 Static Analysis</h3>
            <pre>${JSON.stringify(data.static_analysis, null, 2)}</pre>

            <h3>💡 Suggestion</h3>
            <pre>${JSON.stringify(data.suggestion, null, 2)}</pre>

            <h3>✨ Auto Fix</h3>
            <pre>${data.auto_fix}</pre>

            <h3>📄 Final Report</h3>
            <pre>${data.report}</pre>
        `;

        autofixBtn.classList.remove("d-none");
        pdfBtn.classList.remove("d-none");
    });
});
