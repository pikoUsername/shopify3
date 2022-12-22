all APIs listed here 

    Users: 
        auth: ... 
        users: 
            ... 
            /delete-account(actually deactivating it)
        users-customization:
            (See users customization list)
            / <setting(-s)> # update
            /set-image
            /reset 

    Shop: 
        search-engine: 
            TODO

        product(what users can do with the product): 
            /get_info  
            /buy -> to other api 
            /rate
            /report <reason> 
        seller: 
            product(what seller can do with the product): 
                /set-image 
                /remove
                /hide
                /set-open-date <date>
                /set-close-date <date>
                /create <data>
                /set-tags <tags>
                /change <product's setting(-s)>

    Admin panel: 
        CRUD Model for each model(except user(no update, remove))

    CDN: 
        /upload [image]
        /download <url | id | dir>
