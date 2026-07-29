const API_BASE_URL = "http://127.0.0.1:8000";

const jobForm = document.getElementById("jobForm");
const jobList = document.getElementById("jobList");
const statusText = document.getElementById("statusText");
const refreshBtn = document.getElementById("refreshBtn");
const submitBtn = document.getElementById("submitBtn");
const cancelEditBtn = document.getElementById("cancelEditBtn");

const companyInput = document.getElementById("company");
const positionInput = document.getElementById("position");
const statusInput = document.getElementById("status");
const applyDateInput = document.getElementById("applyDate");
const jobUrlInput = document.getElementById("jobUrl");
const noteInput = document.getElementById("note");

let editingJobId = null;
let currentJobs = [];

function setStatus(message) {
    statusText.textContent = message;
}

function getJobFormData() {
    return {
        company: companyInput.value.trim(),
        position: positionInput.value.trim(),
        status: statusInput.value,
        apply_date: applyDateInput.value || null,
        job_url: jobUrlInput.value.trim() || null,
        note: noteInput.value.trim() || null,
    };
}

function resetFormMode() {
    editingJobId = null;
    jobForm.reset();
    submitBtn.textContent = "保存岗位";
    cancelEditBtn.hidden = true;
}

function startEditJob(job) {
    editingJobId = job.id;

    companyInput.value = job.company;
    positionInput.value = job.position;
    statusInput.value = job.status;
    applyDateInput.value = job.apply_date || "";
    jobUrlInput.value = job.job_url || "";
    noteInput.value = job.note || "";

    submitBtn.textContent = "更新岗位";
    cancelEditBtn.hidden = false;
    setStatus(`正在编辑：${job.company} - ${job.position}`);
}

function renderJobs(jobs) {
    jobList.innerHTML = "";

    if (jobs.length === 0) {
        setStatus("暂无岗位记录");
        return;
    }

    jobs.forEach((job) => {
        const card = document.createElement("article");
        card.className = "job-card";

        const jobLink = job.job_url
            ? `<a class="job-link" href="${job.job_url}" target="_blank" rel="noopener noreferrer">查看岗位链接</a>`
            : "暂无岗位链接";

        card.innerHTML = `
            <div class="job-card-header">
                <div>
                    <h3>${job.company} - ${job.position}</h3>
                    <p>${job.note || "暂无备注"}</p>
                </div>
                <span class="status-badge">${job.status}</span>
            </div>

            <div class="job-meta">
                <p>投递日期：${job.apply_date || "未填写"}</p>
                <p>${jobLink}</p>
            </div>

            <div class="card-actions">
                <button class="edit-btn" data-id="${job.id}">编辑</button>
                <button class="delete-btn" data-id="${job.id}">删除</button>
            </div>
        `;

        jobList.appendChild(card);
    });
}

async function fetchJobs() {
    setStatus("正在加载岗位列表...");

    try {
        const response = await fetch(`${API_BASE_URL}/jobs`);
        if (!response.ok) {
            throw new Error("获取岗位列表失败");
        }

        const jobs = await response.json();
        currentJobs = jobs;
        renderJobs(jobs);
        setStatus(`共 ${jobs.length} 条岗位记录`);
    } catch (error) {
        setStatus("加载失败，请确认后端服务已启动");
    }
}

async function saveJob(event) {
    event.preventDefault();

    const jobData = getJobFormData();
    const isEditing = editingJobId !== null;
    const url = isEditing
        ? `${API_BASE_URL}/jobs/${editingJobId}`
        : `${API_BASE_URL}/jobs`;
    const method = isEditing ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(jobData),
        });

        if (!response.ok) {
            throw new Error(isEditing ? "更新岗位失败" : "新增岗位失败");
        }

        setStatus(isEditing ? "岗位更新成功" : "岗位保存成功");
        resetFormMode();
        await fetchJobs();
    } catch (error) {
        setStatus(isEditing ? "更新失败，请稍后再试" : "保存失败，请检查表单内容或后端服务");
    }
}

async function deleteJob(jobId) {
    try {
        const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            throw new Error("删除岗位失败");
        }

        setStatus("岗位删除成功");
        await fetchJobs();
    } catch (error) {
        setStatus("删除失败，请稍后再试");
    }
}

jobForm.addEventListener("submit", saveJob);
refreshBtn.addEventListener("click", fetchJobs);
cancelEditBtn.addEventListener("click", resetFormMode);

jobList.addEventListener("click", (event) => {
    const jobId = Number(event.target.dataset.id);

    if (event.target.classList.contains("edit-btn")) {
        const job = currentJobs.find((item) => item.id === jobId);
        if (job) {
            startEditJob(job);
        }
    }

    if (event.target.classList.contains("delete-btn")) {
        deleteJob(jobId);
    }
});

fetchJobs();
