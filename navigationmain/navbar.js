document.addEventListener("DOMContentLoaded", function () {
	const mobileMenuIcon = document.getElementById("mobile-menu-icon");
	const mobileNav = document.getElementById("mobile-nav");
  
	if (!mobileMenuIcon || !mobileNav) {
	  console.error("Mobile menu elements not found; please check your template.");
	  return;
	}
  
	// Toggle the mobile navigation overlay when the hamburger icon is clicked
	mobileMenuIcon.addEventListener("click", function() {
	  mobileNav.classList.toggle("active");
	});
  
	// Optional: Close the mobile nav when any link is clicked
	const mobileNavLinks = document.querySelectorAll(".mobile-nav-menu li a");
	mobileNavLinks.forEach(function(link) {
	  link.addEventListener("click", function() {
		mobileNav.classList.remove("active");
	  });
	});
  });
  