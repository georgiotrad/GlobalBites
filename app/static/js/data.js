const restaurants = [

    // ── LEBANESE ──────────────────────────────────────────────
    {
        id: 1,
        name: "Swiss Butter",
        cuisine: "Lebanese",
        rating: 4.9,
        price: "$$$",
        location: "Jal El Dib Main Road, Jal el Dib",
        phone: "+961 4 712 571",
        hours: "12:00 PM – 11:30 PM",
        about: "Swiss Butter is Beirut's most celebrated steakhouse, famous for its signature butter-basted cuts and warm, wood-paneled atmosphere. Every dish is crafted with locally sourced produce and prime cuts that keep guests coming back.",
        images: [
            "../static/img/restaurants/swiss-butter-1.jpg",
            "../static/img/restaurants/swiss-butter-2.jpg",
            "../static/img/restaurants/swiss-butter-3.jpg",
            "../static/img/restaurants/swiss-butter-4.jpg"
        ]
    },
    {
        id: 2,
        name: "Al Shams",
        cuisine: "Lebanese",
        rating: 4.8,
        price: "$$",
        location: "Haouch Moussa, Anjar, Bekaa Valley",
        phone: "+961 8 620 567",
        hours: "12:00 PM – 2:00 AM",
        about: "Established in 1975 in the heart of the Bekaa Valley, Al Shams invites you to enjoy a relaxing atmosphere, delicious traditional Lebanese food, and impeccable service in a beautiful natural setting.",
        images: [
            "../static/img/restaurants/al-shams-1.jpg",
            "../static/img/restaurants/al-shams-2.jpg"
        ]
    },
    {
        id: 3,
        name: "Amaleen",
        cuisine: "Lebanese",
        rating: 4.7,
        price: "$$$",
        location: "Cascada Mall Lakeside, Taanayel",
        phone: "+961 81 600 000",
        hours: "12:00 PM – 12:00 AM",
        about: "Amaleen is a modern Lebanese dining destination blending traditional recipes with a contemporary twist. Known for its vibrant atmosphere, creative presentation, and rich authentic flavors.",
        images: [
            "../static/img/restaurants/amaleen-1.jpg",
            "../static/img/restaurants/amaleen-2.jpg",
            "../static/img/restaurants/amaleen-3.jpg",
            "../static/img/restaurants/amaleen-4.jpg",
            "../static/img/restaurants/amaleen-5.jpg"
        ]
    },

    // ── CHINESE ───────────────────────────────────────────────
    {
        id: 4,
        name: "Totori",
        cuisine: "Chinese",
        rating: 4.7,
        price: "$$",
        location: "513, Mir Omar, Clemenceau, Beirut",
        phone: "+961 81 732 086",
        hours: "12:00 PM – 11:00 PM",
        about: "A delightful Asian bistronomic-style restaurant in the heart of Clemenceau, Beirut. Offering an eclectic mix of Thai, Korean, Chinese and Vietnamese cuisine with fresh, high-quality ingredients at affordable prices.",
        images: [
            "../static/img/restaurants/totori-1.jpg",
            "../static/img/restaurants/totori-2.jpg",
            "../static/img/restaurants/totori-3.jpg",
            "../static/img/restaurants/totori-4.jpg"
        ]
    },
    {
        id: 5,
        name: "Chop Suey",
        cuisine: "Chinese",
        rating: 4.8,
        price: "$$",
        location: "Jounieh - Beirut Hwy, Dbayeh",
        phone: "+961 3 477 667",
        hours: "12:00 PM – 12:00 AM",
        about: "A beloved dining destination driven by passion and culinary excellence. Chop Suey offers an authentic Chinese experience with unforgettable flavors and warm hospitality in Dbayeh.",
        images: [
            "../static/img/restaurants/chop-suey-1.jpg",
            "../static/img/restaurants/chop-suey-2.jpg",
            "../static/img/restaurants/chop-suey-3.jpg",
            "../static/img/restaurants/chop-suey-4.jpg"
        ]
    },

    // ── MEXICAN ───────────────────────────────────────────────
    {
        id: 6,
        name: "Alma Beirut",
        cuisine: "Mexican",
        rating: 4.6,
        price: "$$$",
        location: "Bossa Nova Hotel, Charles Helou, Beirut",
        phone: "+961 1 483 183",
        hours: "12:00 PM – 10:30 PM",
        about: "A tribute to the fearless spirit of South American food. Alma offers vibrant, colourful dishes bursting with intense flavors — a succulent sensory adventure for those who believe food should be consumed with passion.",
        images: [
            "../static/img/restaurants/alma-beirut-1.jpg",
            "../static/img/restaurants/alma-beirut-2.jpg",
            "../static/img/restaurants/alma-beirut-3.jpg",
            "../static/img/restaurants/alma-beirut-4.jpg"
        ]
    },
    {
        id: 7,
        name: "Papa's Mia Tacos",
        cuisine: "Mexican",
        rating: 4.6,
        price: "$$",
        location: "Beirut",
        phone: "+961 78 993 473",
        hours: "12:00 PM – 10:30 PM",
        about: "Beirut's go-to spot for authentic Mexican street-style tacos. Bursting with bold flavors, fresh ingredients, and a lively atmosphere that brings the spirit of Mexico straight to your plate.",
        images: [
            "../static/img/restaurants/papas-mia-tacos-1.jpg",
            "../static/img/restaurants/papas-mia-tacos-2.jpg",
            "../static/img/restaurants/papas-mia-tacos-3.jpg"
        ]
    },

    // ── JAPANESE ──────────────────────────────────────────────
    {
        id: 8,
        name: "Momaki",
        cuisine: "Japanese",
        rating: 4.5,
        price: "$$",
        location: "Dbayeh",
        phone: "www.monmakiamoi.com",
        hours: "12:00 PM – 11:00 PM",
        about: "A unique eco-friendly sushi concept combining a personal touch and refined identity. Known for its white marble fresh bar, live chefs, natural green walls and high-quality sushi for lovers of the Japanese culinary art.",
        images: [
            "../static/img/restaurants/momaki-1.jpg",
            "../static/img/restaurants/momaki-2.jpg",
            "../static/img/restaurants/momaki-3.jpg"
        ]
    },
    {
        id: 9,
        name: "Kami",
        cuisine: "Japanese",
        rating: 4.6,
        price: "$$",
        location: "Main Road, Byblos",
        phone: "+961 3 535 419",
        hours: "12:00 PM – 11:30 PM",
        about: "The best sushi in north Lebanon. Kami is renowned for its consistently fresh fish and expertly crafted rolls, drawing crowds of sushi enthusiasts seeking an authentic Japanese dining experience by the sea.",
        images: [
            "../static/img/restaurants/kami-1.jpg",
            "../static/img/restaurants/kami-2.jpg",
            "../static/img/restaurants/kami-3.jpg",
            "../static/img/restaurants/kami-4.jpg"
        ]
    },

    // ── ITALIAN ───────────────────────────────────────────────
    {
        id: 10,
        name: "Appetito Trattoria",
        cuisine: "Italian",
        rating: 4.5,
        price: "$$",
        location: "Pasteur Street, Beirut",
        phone: "+961 3 682 600",
        hours: "12:00 PM – 11:00 PM",
        about: "A cozy Italian trattoria nestled on Pasteur Street, Beirut. Appetito serves hearty, home-style Italian dishes crafted with fresh ingredients and genuine passion for the Mediterranean culinary tradition.",
        images: [
            "../static/img/restaurants/appetito-trattoria-1.jpg",
            "../static/img/restaurants/appetito-trattoria-2.jpg",
            "../static/img/restaurants/appetito-trattoria-3.jpg",
            "../static/img/restaurants/appetito-trattoria-4.jpg"
        ]
    },
    {
        id: 11,
        name: "Pertutti",
        cuisine: "Italian",
        rating: 4.6,
        price: "$$",
        location: "Martakla, Baabda",
        phone: "+961 5 457 000",
        hours: "12:00 PM – 11:30 PM",
        about: "Your cozy neighborhood corner for authentic Italian cuisine. From heartwarming pastas to fire-baked pizzas, Pertutti crafts every dish with fresh ingredients and Italian passion — a place just like home.",
        images: [
            "../static/img/restaurants/pertutti-1.jpg",
            "../static/img/restaurants/pertutti-2.jpg",
            "../static/img/restaurants/pertutti-3.jpg",
            "../static/img/restaurants/pertutti-4.jpg"
        ]
    }

];
