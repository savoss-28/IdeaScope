/**
 * IdeaScope – Client-side JavaScript
 * Handles loading overlay, complexity slider, score animations,
 * and auto-dismiss alerts.
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Complexity Slider ──────────────────────────────────────────────────
    const complexitySlider = document.getElementById('idea-complexity');
    const complexityValue = document.getElementById('complexity-value');

    if (complexitySlider && complexityValue) {
        complexitySlider.addEventListener('input', function () {
            complexityValue.textContent = this.value;
        });
    }

    // ── Loading Overlay on Form Submit ─────────────────────────────────────
    const ideaForm = document.getElementById('idea-form');
    const loadingOverlay = document.getElementById('loading-overlay');
    const loadingStatus = document.getElementById('loading-status');
    const analyzeBtn = document.getElementById('analyze-submit-btn');

    if (ideaForm && loadingOverlay) {
        ideaForm.addEventListener('submit', function (e) {
            // Show loading overlay
            loadingOverlay.style.display = 'flex';

            // Disable submit button
            if (analyzeBtn) {
                const btnText = analyzeBtn.querySelector('.btn-text');
                const btnLoader = analyzeBtn.querySelector('.btn-loader');
                if (btnText) btnText.style.display = 'none';
                if (btnLoader) btnLoader.style.display = 'flex';
                analyzeBtn.disabled = true;
            }

            // Animate loading status messages
            const statusMessages = [
                'Fetching GitHub repositories...',
                'Extracting keywords with TF-IDF...',
                'Computing cosine similarity...',
                'Calculating uniqueness score...',
                'Analyzing feasibility...',
                'Measuring real-world impact...',
                'Evaluating innovation level...',
                'Generating final report...'
            ];

            let statusIndex = 0;
            const statusInterval = setInterval(function () {
                statusIndex++;
                if (statusIndex < statusMessages.length && loadingStatus) {
                    loadingStatus.textContent = statusMessages[statusIndex];
                }
                if (statusIndex >= statusMessages.length) {
                    clearInterval(statusInterval);
                }
            }, 1200);
        });
    }

    // ── Animated Score Counters ────────────────────────────────────────────
    const scoreValues = document.querySelectorAll('.score-card-value[data-target]');

    scoreValues.forEach(function (el) {
        const target = parseInt(el.getAttribute('data-target'), 10);
        if (isNaN(target)) return;

        let current = 0;
        const increment = target / 60;
        const duration = 1500;
        const frameRate = 1000 / 60;

        const counter = setInterval(function () {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(counter);
            }
            el.textContent = Math.round(current);
        }, frameRate);
    });

    // ── Overall Score Ring Counter ─────────────────────────────────────────
    const ringValue = document.querySelector('.score-ring-value[data-target]');
    if (ringValue) {
        const target = parseFloat(ringValue.getAttribute('data-target'));
        let current = 0;
        const increment = target / 60;

        const counter = setInterval(function () {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(counter);
            }
            ringValue.textContent = Math.round(current);
        }, 1000 / 60);
    }

    // ── Animate Score Ring SVG ─────────────────────────────────────────────
    const ringFill = document.querySelector('.score-ring-fill');
    if (ringFill) {
        const score = ringFill.getAttribute('data-score');
        if (score) {
            // Circumference = 2 * PI * r = 2 * 3.14159 * 52 ≈ 327
            const circumference = 2 * Math.PI * 52;
            const offset = circumference - (score / 100) * circumference;
            
            setTimeout(function () {
                ringFill.style.strokeDasharray = circumference + '';
                ringFill.style.strokeDashoffset = offset + '';
                ringFill.style.transition = 'stroke-dashoffset 1.5s ease-out';
            }, 100);
        }
    }

    // ── Auto-dismiss Alerts ───────────────────────────────────────────────
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // ── Smooth form validation feedback ───────────────────────────────────
    const requiredInputs = document.querySelectorAll('input[required], textarea[required]');
    requiredInputs.forEach(function (input) {
        input.addEventListener('invalid', function (e) {
            e.preventDefault();
            input.style.borderColor = '#ff4c4c';
            input.style.boxShadow = '0 0 0 3px rgba(255, 76, 76, 0.1)';
            
            setTimeout(function () {
                input.style.borderColor = '';
                input.style.boxShadow = '';
            }, 2000);
        });
    });
});

// Tab Switching Logic for IIVP Dashboard
function openTab(evt, tabId) {
    const tabPanes = document.querySelectorAll('.iivp-tab-pane');
    tabPanes.forEach(pane => pane.classList.remove('active'));

    const tabBtns = document.querySelectorAll('.iivp-tab-btn');
    tabBtns.forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabId).classList.add('active');
    evt.currentTarget.classList.add('active');
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize IIVP Score Breakdown Chart if canvas exists
    const canvas = document.getElementById('scoreBreakdownChart');
    if (canvas) {
        try {
            const uniq = JSON.parse(document.getElementById('score-uniq').textContent);
            const feas = JSON.parse(document.getElementById('score-feas').textContent);
            const imp = JSON.parse(document.getElementById('score-imp').textContent);
            const inno = JSON.parse(document.getElementById('score-inno').textContent);
            
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Uniqueness', 'Feasibility', 'Impact', 'Innovation'],
                    datasets: [{
                        label: 'Score',
                        data: [uniq, feas, imp, inno],
                        backgroundColor: [
                            '#00f0ff', // Cyan
                            '#ffcc00', // Yellow
                            '#0088ff', // Blue
                            '#b388ff'  // Purple
                        ],
                        borderWidth: 0,
                        borderRadius: 2
                    }]
                },
                options: {
                    indexAxis: 'y', // This makes it horizontal in Chart.js v3+
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1E1E2C',
                            titleColor: '#00f0ff',
                            bodyFont: { family: "'Inter', sans-serif" }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            max: 100,
                            grid: { color: 'rgba(255, 255, 255, 0.05)' },
                            ticks: { color: '#8892b0' }
                        },
                        y: {
                            grid: { display: false },
                            ticks: { color: '#8892b0', font: { family: "'Inter', sans-serif" } }
                        }
                    }
                }
            });
        } catch(e) {
            console.error("Could not load chart data: ", e);
        }
    }
});
