document.addEventListener('DOMContentLoaded', () => {
    const burgerMenu = document.querySelector('.home-burger-menu');
    const mobileMenu = document.querySelector('.home-mobile-menu');
    const closeMenu = document.querySelector('.home-menu-close');
  
    // Open mobile menu
    burgerMenu.addEventListener('click', () => {
      mobileMenu.style.display = 'block';
    });
  
    // Close mobile menu
    closeMenu.addEventListener('click', () => {
      mobileMenu.style.display = 'none';
    });
  });

import BlazeSlider from 'blaze-slider';

document.addEventListener('DOMContentLoaded', () => {
    const slider = new BlazeSlider(document.querySelector('.blaze-slider'));
  });

  document.addEventListener('DOMContentLoaded', () => {
    const video = document.querySelector('.home-video');
    
    video.setAttribute('playsinline', true);
    video.setAttribute('autoplay', true);
    video.muted = true;
  });


const tabs = document.querySelectorAll(".slide-title");
const banners = document.querySelectorAll(".banner");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const category = tab.getAttribute("data-category");

      tabs.forEach(t => t.classList.remove("slide-title-active"));
      tab.classList.add("slide-title-active");

      banners.forEach(banner => {
        if (banner.getAttribute("data-category") === category) {
          banner.classList.add("active-banner");
        } else {
          banner.classList.remove("active-banner");
        }
      });
    });
  });


  
  
