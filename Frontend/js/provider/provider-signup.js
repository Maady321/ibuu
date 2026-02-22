document.addEventListener("DOMContentLoaded", async () => {
  const serviceSelect = document.getElementById("service");
  const form = document.getElementById("signup-form");

  // 1. Fetch available services for the dropdown
  try {
    const response = await makeRequest("/api/services");
    if (response.ok) {
      const services = await response.json();
      serviceSelect.innerHTML =
        '<option value="">Select Service Specialty</option>';
      services.forEach((service) => {
        const option = document.createElement("option");
        option.value = service.id;
        option.textContent = service.name;
        serviceSelect.appendChild(option);
      });
    } else {
      serviceSelect.innerHTML =
        '<option value="">Error loading specialties</option>';
    }
  } catch (error) {
    console.error("Error fetching services:", error);
    serviceSelect.innerHTML =
      '<option value="">Network error loading services</option>';
  }

  // 2. Form Submission Handler
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Reset previous errors
    const inputs = form.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => window.HB.clearError(input.id));

    const fullname = document.getElementById("fullname").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const dob = document.getElementById("dob").value;
    const address = document.getElementById("address").value.trim();
    const serviceId = document.getElementById("service").value;
    const experience = document.getElementById("experience").value;
    const specialization = document
      .getElementById("specialization")
      .value.trim();
    const bio = document.getElementById("bio").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    // 3. Client-Side Validation
    let hasError = false;

    if (!fullname) {
      window.HB.showError("fullname", "Full name is required");
      hasError = true;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      window.HB.showError("email", "Valid email required");
      hasError = true;
    }

    if (phone.length < 10) {
      window.HB.showError("phone", "Valid phone number required");
      hasError = true;
    }

    if (!dob) {
      window.HB.showError("dob", "Date of birth is required");
      hasError = true;
    }

    if (!serviceId) {
      window.HB.showError("service", "Please select your primary service");
      hasError = true;
    }

    if (!experience || experience < 0) {
      window.HB.showError("experience", "Experience is required");
      hasError = true;
    }

    if (password.length < 6) {
      window.HB.showError("password", "Password must be at least 6 chars");
      hasError = true;
    }

    if (password !== confirmPassword) {
      window.HB.showError("confirm-password", "Passwords do not match");
      hasError = true;
    }

    if (hasError) {
      window.HB.showToast("Please fix the highlighted errors.", "error");
      return;
    }

    // 4. UI State: Loading
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML =
      '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing Application...';

    const formData = {
      full_name: fullname,
      email: email,
      phone: phone,
      dob: dob,
      address: address,
      service_id: parseInt(serviceId),
      years_experience: parseInt(experience),
      specialization: specialization,
      bio: bio,
      password: password,
      id_proof: "pre-registration_v1",
      certificate: "pre-registration_v1",
    };

    try {
      const response = await makeRequest("/api/providers/create", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        window.HB.showToast(
          "Application submitted! Redirecting to login...",
          "success",
        );
        setTimeout(() => {
          window.location.href = "provider-login.html";
        }, 2000);
      } else {
        const result = await response.json();
        const msg = result.detail || "Signup failed. Please try again.";
        window.HB.showToast(msg, "error");

        if (msg.toLowerCase().includes("email"))
          window.HB.showError("email", msg);
        if (msg.toLowerCase().includes("phone"))
          window.HB.showError("phone", msg);
      }
    } catch (error) {
      console.error("Signup Error:", error);
      window.HB.showToast("Connection lost. Please try again.", "error");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalText;
    }
  });
});
