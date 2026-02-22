document
  .getElementById("register-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    // 1. Get Form Data
    const name = document.getElementById("Name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const address = document.getElementById("address").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // 2. Client-Side Validation
    let hasError = false;

    if (name.length < 2) {
      window.HB.showError("Name", "Name must be at least 2 characters.");
      hasError = true;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      window.HB.showError("email", "Please enter a valid email address.");
      hasError = true;
    }

    if (phone.length < 10) {
      window.HB.showError("phone", "Please enter a valid phone number.");
      hasError = true;
    }

    if (password.length < 6) {
      window.HB.showError(
        "password",
        "Password must be at least 6 characters.",
      );
      hasError = true;
    }

    if (password !== confirmPassword) {
      window.HB.showError("confirmPassword", "Passwords do not match.");
      hasError = true;
    }

    if (hasError) return;

    // 3. UI State: Loading
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML =
      '<i class="fa-solid fa-circle-notch fa-spin"></i> Creating Account...';

    try {
      const response = await makeRequest("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({
          name,
          email,
          phone,
          address,
          password,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        window.HB.showToast(
          result.message || "Registration successful!",
          "success",
        );

        // Auto-login or redirect
        setTimeout(() => {
          window.location.href = "login.html?registered=true";
        }, 2000);
      } else {
        // Handle specific backend errors
        const errorMsg =
          result.detail || "Registration failed. Please try again.";
        window.HB.showToast(errorMsg, "error");

        // If the error is field-specific, try to highlight it
        if (errorMsg.toLowerCase().includes("email")) {
          window.HB.showError("email", errorMsg);
        } else if (errorMsg.toLowerCase().includes("phone")) {
          window.HB.showError("phone", errorMsg);
        }
      }
    } catch (error) {
      console.error("Registration Error:", error);
      window.HB.showToast(
        "Server connection failed. Please check your internet.",
        "error",
      );
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
