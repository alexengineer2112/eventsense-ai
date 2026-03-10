async function loadJobs(){

    const response = await fetch("http://localhost:5000/jobs");
    const jobs = await response.json();

    const container = document.getElementById("jobs");

    container.innerHTML = "";

    if(jobs.length === 0){
        container.innerHTML = "No placement updates available.";
        return;
    }

    jobs.forEach(job => {

        const div = document.createElement("div");
        div.className = "job";

        let deadlineHTML = "";

        if(job.deadline){
            deadlineHTML = `<div class="deadline">Deadline: ${job.deadline}</div>`;
        }

        let applyButton = "";

        if(job.application_links && job.application_links.length > 0){
            applyButton = `<a class="apply" href="${job.application_links[0]}" target="_blank">Apply</a>`;
        }

        let title = job.company ? job.company : "📢 Announcement";

        let role = job.job_role ? job.job_role : (job.summary || "");

        div.innerHTML = `
            <div class="company">${title}</div>
            <div class="role">${role}</div>
            ${deadlineHTML}
            ${applyButton}
        `;

        container.appendChild(div);

    });

}

loadJobs();