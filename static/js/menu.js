document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById("menu-btn");
  const menu = document.getElementById("menu");

  if (menuBtn && menu) {
    menuBtn.addEventListener("click", () => {
      menu.classList.toggle("hidden");
      menu.classList.toggle("flex");
    });

    // Cerrar el menú al hacer clic en cualquier enlace (en móvil)
    const links = menu.querySelectorAll("a");
    links.forEach(link => {
      link.addEventListener("click", () => {
        if (window.innerWidth < 768) {
          menu.classList.add("hidden");
          menu.classList.remove("flex");
        }
      });
    });
  }
});
