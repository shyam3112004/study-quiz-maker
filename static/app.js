/**
 * Study Quiz Maker - Client Application (Doc 04 App Flow & Doc 07 Implementation)
 */

(function () {
  "use strict";

  // State Management
  const state = {
    notes: "",
    numQuestions: 5,
    difficulty: "medium",
    maxChars: 6000,
    minChars: 20,
    currentQuiz: null,
    currentQuestionIndex: 0,
    score: 0,
    userAnswers: [], // Stores { question, options, selectedIndex, correctIndex, explanation, isCorrect }
    hasAnsweredCurrent: false,
    isGenerating: false,
  };

  // Sample Note Presets for Instant Testing
  const SAMPLES = {
    biology: `Photosynthesis is the biological process used by plants, algae, and certain bacteria to harness energy from sunlight and turn it into chemical energy.
The process takes place inside plant cell organelles called chloroplasts. Chloroplasts contain chlorophyll, the green pigment that absorbs light wavelengths.
Photosynthesis consists of two distinct stages:
1. The Light-Dependent Reactions: Take place across the thylakoid membranes inside the chloroplast. Sunlight excites electrons in chlorophyll within Photosystems II and I. Water molecules (H2O) are split into oxygen gas, protons, and electrons through photolysis. This reaction drives ATP synthesis via chemiosmosis and reduces NADP+ to form NADPH. Oxygen is released into the atmosphere as a byproduct.
2. The Calvin Cycle (Light-Independent Reactions): Occurs in the stroma of the chloroplast. The enzyme RuBisCO catalyzes the fixation of carbon dioxide (CO2) onto ribulose 1,5-bisphosphate (RuBP). Using ATP and NADPH from the light stage, 3-PGA is reduced into glyceraldehyde-3-phosphate (G3P), which is subsequently used to synthesize glucose and regenerate RuBP.`,

    cs: `Big-O Notation is used in computer science to classify algorithms according to how their run time or space requirements grow as the input size (n) increases.
Key Complexity Classes from best to worst:
- O(1) - Constant Time: The execution time remains unchanged regardless of input size (e.g., accessing an element in an array by index, hash table lookup in the average case).
- O(log n) - Logarithmic Time: The problem size is divided by a constant factor in each step (e.g., binary search on a sorted array).
- O(n) - Linear Time: Operations grow proportionally with input size (e.g., simple linear search, traversing a linked list).
- O(n log n) - Linearithmic Time: Efficient divide-and-conquer sorting algorithms (e.g., Merge Sort, Heapsort, QuickSort average case).
- O(n^2) - Quadratic Time: Typical of algorithms with nested loops over the data set (e.g., Bubble Sort, Insertion Sort worst case).
Space complexity evaluates the additional auxiliary memory required by an algorithm during execution beyond the input itself.`,

    history: `The Industrial Revolution was the transition to new manufacturing processes in Great Britain, continental Europe, and the United States that occurred from roughly 1760 to 1840.
Key Factors and Innovations:
1. Steam Power: James Watt's improvements to the Newcomen steam engine in 1776 drastically boosted efficiency, allowing factories to be powered away from fast-flowing rivers.
2. Textile Mechanization: Inventions such as James Hargreaves' Spinning Jenny, Richard Arkwright's Water Frame, and Samuel Crompton's Spinning Mule increased cotton and textile production exponentially.
3. Iron and Coal: Smelting iron ore with coke instead of charcoal allowed for cheaper, stronger iron needed for bridges, railways, and machinery.
4. Social Impact: Caused massive urbanization as agricultural workers migrated to industrial cities like Manchester and Birmingham, creating new social classes and prompting early labor reform movements.`,
  };

  // DOM Element Selectors
  const dom = {
    notesInput: document.getElementById("notes-input"),
    charCount: document.getElementById("char-count"),
    charMax: document.getElementById("char-max"),
    charCounterBar: document.getElementById("char-counter-bar"),
    generateBtn: document.getElementById("generate-btn"),
    generateBtnText: document.getElementById("generate-btn-text"),
    pasteFeedback: document.getElementById("paste-feedback"),
    qCountGroup: document.getElementById("q-count-group"),
    difficultyGroup: document.getElementById("difficulty-group"),
    sampleBioBtn: document.getElementById("sample-bio-btn"),
    sampleCsBtn: document.getElementById("sample-cs-btn"),
    sampleHistoryBtn: document.getElementById("sample-history-btn"),
    quickDemoBtn: document.getElementById("quick-demo-btn"),
    quizEmptyView: document.getElementById("quiz-empty-view"),
    quizLoadingView: document.getElementById("quiz-loading-view"),
    quizPlayerView: document.getElementById("quiz-player-view"),
    qCounterText: document.getElementById("q-counter-text"),
    qDifficultyBadge: document.getElementById("q-difficulty-badge"),
    quizProgressFill: document.getElementById("quiz-progress-fill"),
    questionText: document.getElementById("question-text"),
    optionsContainer: document.getElementById("options-container"),
    explanationBox: document.getElementById("explanation-box"),
    expStatusTitle: document.getElementById("exp-status-title"),
    expContent: document.getElementById("exp-content"),
    nextBtn: document.getElementById("next-btn"),
    finalScoreVal: document.getElementById("final-score-val"),
    finalTotalVal: document.getElementById("final-total-val"),
    scoreSubmessage: document.getElementById("score-submessage"),
    retryBtn: document.getElementById("retry-btn"),
    reviewToggleBtn: document.getElementById("review-toggle-btn"),
    reviewChevron: document.getElementById("review-chevron"),
    reviewList: document.getElementById("review-list"),
  };

  // Initialization
  function init() {
    setupCharCounter();
    setupPillControls();
    setupSampleNotes();
    setupQuizEvents();
    setupKeyboardShortcuts();
    setupReviewAccordion();
  }

  // Live Character Counter & Validation
  function setupCharCounter() {
    if (!dom.notesInput) return;

    dom.notesInput.addEventListener("input", function () {
      state.notes = dom.notesInput.value;
      const count = state.notes.length;
      if (dom.charCount) dom.charCount.textContent = count;

      if (count > state.maxChars) {
        dom.charCounterBar.classList.add("error");
      } else {
        dom.charCounterBar.classList.remove("error");
      }

      // Clear inline error if valid
      if (count >= state.minChars && count <= state.maxChars) {
        hideFeedback();
      }
    });
  }

  // Pill Option Selectors
  function setupPillControls() {
    // Question count selector
    if (dom.qCountGroup) {
      dom.qCountGroup.addEventListener("click", function (e) {
        const target = e.target.closest(".pill-option");
        if (!target) return;
        dom.qCountGroup.querySelectorAll(".pill-option").forEach((p) => {
          p.classList.remove("active");
          p.setAttribute("aria-checked", "false");
        });
        target.classList.add("active");
        target.setAttribute("aria-checked", "true");
        state.numQuestions = parseInt(target.getAttribute("data-value"), 10) || 5;
      });
    }

    // Difficulty selector
    if (dom.difficultyGroup) {
      dom.difficultyGroup.addEventListener("click", function (e) {
        const target = e.target.closest(".pill-option");
        if (!target) return;
        dom.difficultyGroup.querySelectorAll(".pill-option").forEach((p) => {
          p.classList.remove("active");
          p.setAttribute("aria-checked", "false");
        });
        target.classList.add("active");
        target.setAttribute("aria-checked", "true");
        state.difficulty = target.getAttribute("data-value") || "medium";
      });
    }
  }

  // Sample Notes Filling
  function setupSampleNotes() {
    function loadSample(key) {
      if (SAMPLES[key] && dom.notesInput) {
        dom.notesInput.value = SAMPLES[key];
        dom.notesInput.dispatchEvent(new Event("input"));
        dom.notesInput.focus();
        showFeedback("Sample notes loaded! Click Generate Quiz to create questions.", "success");
      }
    }

    if (dom.sampleBioBtn) dom.sampleBioBtn.addEventListener("click", () => loadSample("biology"));
    if (dom.sampleCsBtn) dom.sampleCsBtn.addEventListener("click", () => loadSample("cs"));
    if (dom.sampleHistoryBtn) dom.sampleHistoryBtn.addEventListener("click", () => loadSample("history"));

    if (dom.quickDemoBtn) {
      dom.quickDemoBtn.addEventListener("click", () => {
        loadSample("biology");
        const pasteSection = document.getElementById("paste");
        if (pasteSection) pasteSection.scrollIntoView({ behavior: "smooth" });
      });
    }
  }

  // Inline Feedback Banner
  function showFeedback(msg, type = "error") {
    if (!dom.pasteFeedback) return;
    dom.pasteFeedback.textContent = msg;
    dom.pasteFeedback.className = `feedback-banner show ${type}`;
  }

  function hideFeedback() {
    if (!dom.pasteFeedback) return;
    dom.pasteFeedback.className = "feedback-banner";
    dom.pasteFeedback.textContent = "";
  }

  // API Quiz Generation
  async function handleGenerateQuiz() {
    const text = (dom.notesInput ? dom.notesInput.value : "").trim();

    if (text.length < state.minChars) {
      showFeedback(`Please paste at least ${state.minChars} characters of study notes to build a quiz.`);
      dom.notesInput.focus();
      return;
    }

    if (text.length > state.maxChars) {
      showFeedback(`Your notes exceed the maximum limit of ${state.maxChars} characters.`);
      dom.notesInput.focus();
      return;
    }

    hideFeedback();
    setGeneratingState(true);

    // Scroll smoothly to Quiz Section
    const quizSection = document.getElementById("quiz");
    if (quizSection) quizSection.scrollIntoView({ behavior: "smooth" });

    // Show loading skeleton
    if (dom.quizEmptyView) dom.quizEmptyView.style.display = "none";
    if (dom.quizPlayerView) dom.quizPlayerView.style.display = "none";
    if (dom.quizLoadingView) dom.quizLoadingView.style.display = "block";

    try {
      const response = await fetch("/quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          notes: text,
          num_questions: state.numQuestions,
          difficulty: state.difficulty,
        }),
      });

      if (!response.ok) {
        let errDetail = "Failed to generate quiz. Please try again.";
        try {
          const errData = await response.json();
          if (errData.detail) errDetail = errData.detail;
        } catch (_) {}
        throw new Error(errDetail);
      }

      const data = await response.json();

      if (!data.questions || !data.questions.length) {
        throw new Error("No questions were returned. Please try expanding your study notes.");
      }

      // Quiz received successfully!
      state.currentQuiz = data;
      state.currentQuestionIndex = 0;
      state.score = 0;
      state.userAnswers = [];

      startQuizPlayer();
    } catch (err) {
      console.error("Quiz generation error:", err);
      // Reset quiz view
      if (dom.quizLoadingView) dom.quizLoadingView.style.display = "none";
      if (dom.quizEmptyView) dom.quizEmptyView.style.display = "block";

      showFeedback(err.message || "An error occurred while generating the quiz.");
      const pasteSection = document.getElementById("paste");
      if (pasteSection) pasteSection.scrollIntoView({ behavior: "smooth" });
    } finally {
      setGeneratingState(false);
    }
  }

  function setGeneratingState(isGenerating) {
    state.isGenerating = isGenerating;
    if (dom.generateBtn) dom.generateBtn.disabled = isGenerating;
    if (dom.generateBtnText) {
      dom.generateBtnText.textContent = isGenerating ? "Generating Quiz..." : "Generate Quiz →";
    }
  }

  // Quiz Player Logic
  function startQuizPlayer() {
    if (!state.currentQuiz || !state.currentQuiz.questions.length) return;

    if (dom.quizEmptyView) dom.quizEmptyView.style.display = "none";
    if (dom.quizLoadingView) dom.quizLoadingView.style.display = "none";
    if (dom.quizPlayerView) dom.quizPlayerView.style.display = "block";

    renderQuestion();
  }

  function renderQuestion() {
    const qIndex = state.currentQuestionIndex;
    const questions = state.currentQuiz.questions;
    const currentQ = questions[qIndex];

    state.hasAnsweredCurrent = false;

    // Header counter and difficulty
    if (dom.qCounterText) {
      dom.qCounterText.textContent = `Question ${qIndex + 1} of ${questions.length}`;
    }
    if (dom.qDifficultyBadge) {
      dom.qDifficultyBadge.textContent = (state.currentQuiz.difficulty || state.difficulty).toUpperCase();
    }

    // Progress bar
    if (dom.quizProgressFill) {
      const pct = (qIndex / questions.length) * 100;
      dom.quizProgressFill.style.width = `${pct}%`;
    }

    // Question Text
    if (dom.questionText) {
      dom.questionText.textContent = currentQ.question;
    }

    // Reset explanation box and next button
    if (dom.explanationBox) {
      dom.explanationBox.className = "explanation-card";
      dom.explanationBox.style.display = "none";
    }
    if (dom.expContent) dom.expContent.textContent = "";

    if (dom.nextBtn) {
      dom.nextBtn.disabled = true;
      const isLast = qIndex === questions.length - 1;
      dom.nextBtn.textContent = isLast ? "View Score Summary →" : "Next Question →";
    }

    // Render Options
    if (dom.optionsContainer) {
      dom.optionsContainer.innerHTML = "";
      const keys = ["A", "B", "C", "D"];

      currentQ.options.forEach((optText, idx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "option-btn";
        btn.setAttribute("role", "radio");
        btn.setAttribute("aria-checked", "false");
        btn.setAttribute("data-index", idx);
        btn.id = `option-btn-${idx}`;

        const keyBadge = document.createElement("span");
        keyBadge.className = "option-key";
        keyBadge.textContent = keys[idx] || (idx + 1);

        const textSpan = document.createElement("span");
        textSpan.className = "option-text";
        textSpan.textContent = optText;

        btn.appendChild(keyBadge);
        btn.appendChild(textSpan);

        btn.addEventListener("click", () => handleAnswerSelect(idx));
        dom.optionsContainer.appendChild(btn);
      });
    }
  }

  function handleAnswerSelect(selectedIdx) {
    if (state.hasAnsweredCurrent) return; // Prevent multiple clicks
    state.hasAnsweredCurrent = true;

    const currentQ = state.currentQuiz.questions[state.currentQuestionIndex];
    const isCorrect = selectedIdx === currentQ.answer_index;

    if (isCorrect) {
      state.score += 1;
    }

    // Save answer record for summary
    state.userAnswers.push({
      question: currentQ.question,
      options: currentQ.options,
      selectedIndex: selectedIdx,
      correctIndex: currentQ.answer_index,
      explanation: currentQ.explanation,
      isCorrect: isCorrect,
    });

    // Style option buttons
    const allOptionBtns = dom.optionsContainer.querySelectorAll(".option-btn");
    allOptionBtns.forEach((btn, idx) => {
      btn.disabled = true;
      if (idx === currentQ.answer_index) {
        btn.classList.add("correct");
        btn.setAttribute("aria-checked", "true");
      }
      if (idx === selectedIdx && !isCorrect) {
        btn.classList.add("wrong");
      }
    });

    // Reveal Explanation Card
    if (dom.explanationBox) {
      dom.explanationBox.className = `explanation-card show ${isCorrect ? "is-correct" : "is-wrong"}`;
      if (dom.expStatusTitle) {
        dom.expStatusTitle.textContent = isCorrect ? "✓ Correct!" : "✕ Incorrect";
        dom.expStatusTitle.style.color = isCorrect ? "var(--status-correct)" : "var(--status-wrong)";
      }
      if (dom.expContent) {
        dom.expContent.textContent = currentQ.explanation;
      }
    }

    // Enable Next Question button
    if (dom.nextBtn) {
      dom.nextBtn.disabled = false;
      dom.nextBtn.focus();
    }
  }

  function handleNextQuestion() {
    if (!state.hasAnsweredCurrent) return;

    const questions = state.currentQuiz.questions;
    if (state.currentQuestionIndex < questions.length - 1) {
      state.currentQuestionIndex += 1;
      renderQuestion();
    } else {
      // Completed all questions! Show score screen
      showScoreScreen();
    }
  }

  function showScoreScreen() {
    const total = state.currentQuiz.questions.length;
    const score = state.score;
    const pct = Math.round((score / total) * 100);

    // Update progress bar to 100%
    if (dom.quizProgressFill) dom.quizProgressFill.style.width = "100%";

    if (dom.finalScoreVal) dom.finalScoreVal.textContent = score;
    if (dom.finalTotalVal) dom.finalTotalVal.textContent = `/ ${total}`;

    let subMsg = "";
    if (pct === 100) {
      subMsg = "Outstanding mastery! You answered 100% of the questions correctly.";
    } else if (pct >= 80) {
      subMsg = `Great work! You scored ${pct}%. Review the details below to cement full understanding.`;
    } else if (pct >= 60) {
      subMsg = `Solid foundation! You scored ${pct}%. Review the explanations below and give it another try.`;
    } else {
      subMsg = `You scored ${pct}%. Active recall takes repetition—check the explanations below and retry!`;
    }

    if (dom.scoreSubmessage) dom.scoreSubmessage.textContent = subMsg;

    // Build Detailed Review Breakdown
    buildReviewList();

    // Scroll to Score Section
    const scoreSection = document.getElementById("score");
    if (scoreSection) scoreSection.scrollIntoView({ behavior: "smooth" });
  }

  function buildReviewList() {
    if (!dom.reviewList) return;
    dom.reviewList.innerHTML = "";

    state.userAnswers.forEach((ans, idx) => {
      const item = document.createElement("div");
      item.className = "review-item";

      const header = document.createElement("div");
      header.className = "review-item-header";

      const title = document.createElement("div");
      title.className = "review-q-title";
      title.textContent = `Q${idx + 1}: ${ans.question}`;

      const tag = document.createElement("span");
      tag.className = `review-status-tag ${ans.isCorrect ? "correct" : "wrong"}`;
      tag.textContent = ans.isCorrect ? "Correct" : "Missed";

      header.appendChild(title);
      header.appendChild(tag);

      const optsDiv = document.createElement("div");
      optsDiv.className = "review-options";
      optsDiv.innerHTML = `
        <div><strong>Your answer:</strong> ${ans.options[ans.selectedIndex]} ${ans.isCorrect ? "✓" : "✕"}</div>
        ${!ans.isCorrect ? `<div><strong>Correct answer:</strong> ${ans.options[ans.correctIndex]}</div>` : ""}
      `;

      const expDiv = document.createElement("div");
      expDiv.className = "review-exp";
      expDiv.textContent = `💡 ${ans.explanation}`;

      item.appendChild(header);
      item.appendChild(optsDiv);
      item.appendChild(expDiv);

      dom.reviewList.appendChild(item);
    });
  }

  // Setup Review Accordion Toggle
  function setupReviewAccordion() {
    if (!dom.reviewToggleBtn || !dom.reviewList) return;

    dom.reviewToggleBtn.addEventListener("click", () => {
      const isOpen = dom.reviewList.classList.contains("show");
      if (isOpen) {
        dom.reviewList.classList.remove("show");
        dom.reviewToggleBtn.setAttribute("aria-expanded", "false");
        if (dom.reviewChevron) dom.reviewChevron.textContent = "▼";
      } else {
        dom.reviewList.classList.add("show");
        dom.reviewToggleBtn.setAttribute("aria-expanded", "true");
        if (dom.reviewChevron) dom.reviewChevron.textContent = "▲";
      }
    });
  }

  // Retake / Retry Quiz Logic
  function handleRetryQuiz() {
    if (!state.currentQuiz || !state.currentQuiz.questions.length) return;

    // Reset progress
    state.currentQuestionIndex = 0;
    state.score = 0;
    state.userAnswers = [];

    // Shuffle questions slightly for varied retake practice
    state.currentQuiz.questions.sort(() => Math.random() - 0.5);

    startQuizPlayer();

    const quizSection = document.getElementById("quiz");
    if (quizSection) quizSection.scrollIntoView({ behavior: "smooth" });
  }

  // Quiz Events Wiring
  function setupQuizEvents() {
    if (dom.generateBtn) {
      dom.generateBtn.addEventListener("click", handleGenerateQuiz);
    }
    if (dom.nextBtn) {
      dom.nextBtn.addEventListener("click", handleNextQuestion);
    }
    if (dom.retryBtn) {
      dom.retryBtn.addEventListener("click", handleRetryQuiz);
    }
  }

  // Keyboard Navigation: 1-4 for options, Enter for next
  function setupKeyboardShortcuts() {
    document.addEventListener("keydown", function (e) {
      // Ignore if user is currently typing in a textarea or input
      if (e.target.tagName === "TEXTAREA" || e.target.tagName === "INPUT") return;

      // Only active if quiz player is currently displayed
      if (!dom.quizPlayerView || dom.quizPlayerView.style.display === "none") return;

      // Keys '1', '2', '3', '4' to pick options
      if (["1", "2", "3", "4"].includes(e.key)) {
        const optionIdx = parseInt(e.key, 10) - 1;
        handleAnswerSelect(optionIdx);
        e.preventDefault();
      }

      // Enter to advance when answered
      if (e.key === "Enter" && state.hasAnsweredCurrent) {
        handleNextQuestion();
        e.preventDefault();
      }
    });
  }

  // Execute on DOM Ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
