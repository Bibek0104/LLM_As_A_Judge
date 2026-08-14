const API_URL = "http://127.0.0.1:8000";


// ==================================================
// LOGIN
// ==================================================

async function login() {

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    const message =
        document.getElementById("login-message");


    if (!username || !password) {

        message.innerText =
            "Please enter username and password.";

        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                // Allows browser to store/send JWT cookie
                credentials: "include",

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            message.innerText =
                data.detail || "Login failed.";

            return;
        }


        // Login successful

        message.innerText =
            "✓ Login and authorization successful";


        // Show prompt section

        document.getElementById(
            "prompt-section"
        ).style.display = "block";


        // Show logout button

        document.getElementById(
            "logout-section"
        ).style.display = "block";


        // Load previous evaluations

        loadEvaluations();

    }

    catch (error) {

        console.error(error);

        message.innerText =
            "Unable to connect to server.";
    }
}



// ==================================================
// RUN LLM + JUDGE
// ==================================================

async function runJudge() {

    const prompt =
        document.getElementById("prompt").value;


    if (!prompt) {

        alert("Please enter a prompt.");

        return;
    }


    // ==================================================
    // LOADING START
    // ==================================================

    const loading =
        document.getElementById("loading");

    const elapsedTime =
        document.getElementById("elapsed-time");


    loading.style.display = "block";


    // Start elapsed timer

    let seconds = 0;

    elapsedTime.innerText = seconds;


    const timer = setInterval(() => {

        seconds++;

        elapsedTime.innerText = seconds;

    }, 1000);


    // Disable Run button

    const runButton =
        document.querySelector(
            "#prompt-section button"
        );


    runButton.disabled = true;

    runButton.innerText =
        "Processing...";


    // ==================================================
    // START REQUEST TIMER
    // ==================================================

    const startTime =
        performance.now();


    try {

        // ==================================================
        // SEND REQUEST TO FASTAPI
        // ==================================================

        const response = await fetch(
            `${API_URL}/run`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                // Automatically sends JWT cookie

                credentials: "include",

                body: JSON.stringify({
                    prompt: prompt
                })
            }
        );


        // Convert response to JSON

        const data =
            await response.json();


        // ==================================================
        // REQUEST FINISHED
        // ==================================================

        const endTime =
            performance.now();


        const totalTime =
            ((endTime - startTime) / 1000).toFixed(2);


        console.log(
            "Total request time:",
            totalTime,
            "seconds"
        );


        // ==================================================
        // CHECK RESPONSE
        // ==================================================

        if (!response.ok) {

            alert(
                data.detail ||
                "Unable to execute request."
            );

            return;
        }


        // ==================================================
        // SHOW RESULT SECTIONS
        // ==================================================

        document.getElementById(
            "agent-section"
        ).style.display = "block";


        document.getElementById(
            "judge-section"
        ).style.display = "block";


        // ==================================================
        // DISPLAY AGENT RESPONSE
        // ==================================================

        displayAgentResult(
            data.agent
        );


        // ==================================================
        // DISPLAY JUDGE RESPONSE
        // ==================================================

        displayJudgeResult(
            data.judge
        );


        // ==================================================
        // REFRESH DATABASE HISTORY
        // ==================================================

        loadEvaluations();


    }

    catch (error) {

        console.error(
            "Run error:",
            error
        );


        alert(
            "Unable to connect to server."
        );

    }

    finally {

        // ==================================================
        // STOP TIMER
        // ==================================================

        clearInterval(timer);


        // Hide loading section

        loading.style.display = "none";


        // Enable Run button

        runButton.disabled = false;

        runButton.innerText =
            "Run";
    }
}



// ==================================================
// DISPLAY AGENT RESULT
// ==================================================

function displayAgentResult(agent) {

    document.getElementById(
        "agent-response"
    ).innerText =
        agent.response;


    document.getElementById(
        "agent-metrics"
    ).innerHTML = `

        <h3>Metrics</h3>

        <p>
            <b>Agent:</b>
            ${agent.agent_name}
        </p>

        <p>
            <b>Model:</b>
            ${agent.model}
        </p>

        <p>
            <b>Input Tokens:</b>
            ${agent.input_tokens}
        </p>

        <p>
            <b>Output Tokens:</b>
            ${agent.output_tokens}
        </p>

        <p>
            <b>Total Tokens:</b>
            ${agent.total_tokens}
        </p>

        <p>
            <b>Latency:</b>
            ${agent.latency}
            seconds
        </p>

    `;
}



// ==================================================
// DISPLAY JUDGE RESULT
// ==================================================

function displayJudgeResult(judge) {

    const evaluation =
        judge.judge_response;


    let html = "";


    // ==================================================
    // CORRECTNESS
    // ==================================================

    html += `

        <div class="score">

            <h3>
                Correctness:
                ${evaluation.correctness.score}/10
            </h3>

            <p>
                ${evaluation.correctness.explanation}
            </p>

        </div>

    `;


    // ==================================================
    // RELEVANCE
    // ==================================================

    html += `

        <div class="score">

            <h3>
                Relevance:
                ${evaluation.relevance.score}/10
            </h3>

            <p>
                ${evaluation.relevance.explanation}
            </p>

        </div>

    `;


    // ==================================================
    // COMPLETENESS
    // ==================================================

    html += `

        <div class="score">

            <h3>
                Completeness:
                ${evaluation.completeness.score}/10
            </h3>

            <p>
                ${evaluation.completeness.explanation}
            </p>

        </div>

    `;


    // ==================================================
    // CLARITY
    // ==================================================

    html += `

        <div class="score">

            <h3>
                Clarity:
                ${evaluation.clarity.score}/10
            </h3>

            <p>
                ${evaluation.clarity.explanation}
            </p>

        </div>

    `;


    // ==================================================
    // OVERALL
    // ==================================================

    html += `

        <div class="score">

            <h3>
                Overall:
                ${evaluation.overall.score}/10
            </h3>

            <p>
                ${evaluation.overall.explanation}
            </p>

        </div>

    `;


    // Display evaluation

    document.getElementById(
        "judge-response"
    ).innerHTML = html;


    // ==================================================
    // JUDGE METRICS
    // ==================================================

    document.getElementById(
        "judge-metrics"
    ).innerHTML = `

        <h3>Judge Metrics</h3>

        <p>
            <b>Model:</b>
            ${judge.judge_model}
        </p>

        <p>
            <b>Input Tokens:</b>
            ${judge.judge_input_tokens}
        </p>

        <p>
            <b>Output Tokens:</b>
            ${judge.judge_output_tokens}
        </p>

        <p>
            <b>Total Tokens:</b>
            ${judge.judge_total_tokens}
        </p>

        <p>
            <b>Latency:</b>
            ${judge.judge_latency}
            seconds
        </p>

        <p>
            <b>Status:</b>
            ${judge.status}
        </p>

    `;
}



// ==================================================
// LOAD DATABASE HISTORY
// ==================================================

async function loadEvaluations() {

    try {

        const response = await fetch(
            `${API_URL}/evaluations`,
            {
                method: "GET",

                // Automatically sends JWT cookie

                credentials: "include"
            }
        );


        if (!response.ok) {

            console.log(
                "Unable to load evaluations."
            );

            return;
        }


        const evaluations =
            await response.json();


        displayHistory(
            evaluations
        );

    }

    catch (error) {

        console.error(
            "Error loading evaluations:",
            error
        );
    }
}



// ==================================================
// DISPLAY DATABASE HISTORY
// ==================================================

function displayHistory(evaluations) {

    const history =
        document.getElementById(
            "history"
        );


    if (!evaluations.length) {

        history.innerHTML =
            "<p>No previous evaluations.</p>";

        return;
    }


    let html = "";


    evaluations.forEach(
        evaluation => {

            html += `

                <div class="history-item">

                    <h3>
                        ${evaluation.agent_name}
                    </h3>

                    <p>
                        <b>Prompt:</b>
                        ${evaluation.prompt}
                    </p>

                    <p>
                        <b>Model:</b>
                        ${evaluation.model}
                    </p>

                    <p>
                        <b>Input Tokens:</b>
                        ${evaluation.input_tokens}
                    </p>

                    <p>
                        <b>Output Tokens:</b>
                        ${evaluation.output_tokens}
                    </p>

                    <p>
                        <b>Total Tokens:</b>
                        ${evaluation.total_tokens}
                    </p>

                    <p>
                        <b>Latency:</b>
                        ${evaluation.latency}
                        seconds
                    </p>

                    <p>
                        <b>Status:</b>
                        ${evaluation.status}
                    </p>

                </div>

            `;
        }
    );


    history.innerHTML =
        html;


    document.getElementById(
        "history-section"
    ).style.display = "block";
}



// ==================================================
// LOGOUT
// ==================================================

async function logout() {

    try {

        await fetch(
            `${API_URL}/logout`,
            {
                method: "POST",

                credentials: "include"
            }
        );


        // ==================================================
        // HIDE APPLICATION SECTIONS
        // ==================================================

        document.getElementById(
            "prompt-section"
        ).style.display = "none";


        document.getElementById(
            "agent-section"
        ).style.display = "none";


        document.getElementById(
            "judge-section"
        ).style.display = "none";


        document.getElementById(
            "history-section"
        ).style.display = "none";


        document.getElementById(
            "logout-section"
        ).style.display = "none";


        // ==================================================
        // CLEAR INPUTS
        // ==================================================

        document.getElementById(
            "username"
        ).value = "";


        document.getElementById(
            "password"
        ).value = "";


        document.getElementById(
            "prompt"
        ).value = "";


        // ==================================================
        // SHOW LOGOUT MESSAGE
        // ==================================================

        document.getElementById(
            "login-message"
        ).innerText =
            "Logged out successfully.";

    }

    catch (error) {

        console.error(
            "Logout error:",
            error
        );
    }
}