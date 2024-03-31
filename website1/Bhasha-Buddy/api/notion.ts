// import type { NextApiRequest,NextApiResponse } from "next";
// import  { Client } from "@notionhq/client"

// const notion = new Client({

// })
// const notionSecret = process.env.NOTION_SECRET;
// const notionDatabaseID = process.env.NOTION_DATABASE_ID;


// export default async function handler(req:NextApiRequest, res:NextApiResponse) {
//     if(!notionSecret ||  !notionDatabaseID) throw new Error ("missing ids")

//     const query = await notion.databases.query({
//         database_id : notionDatabaseID
//     })
//     console.log(query.results)
// }




import type { NextApiRequest, NextApiResponse } from "next";
import { Client } from "@notionhq/client";

// Ensure you have NOTION_SECRET and NOTION_DATABASE_ID set in your .env.local file
const notionSecret = process.env.NOTION_SECRET;
const notionDatabaseID = process.env.NOTION_DATABASE_ID;

// Initialize the Notion client inside the handler to use the environment variables correctly
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    // Check if the necessary environment variables are set
    if (!notionSecret || !notionDatabaseID) {
        // If not, return an error response
        res.status(500).json({ error: "Server configuration error: missing Notion API credentials." });
        return; // Stop execution
    }

    // Initialize the Notion client with the secret
    const notion = new Client({ auth: notionSecret });

    try {
        const query = await notion.databases.query({
            database_id: notionDatabaseID,
        });
        console.log(query.results);

        // Send the query results back to the client
        res.status(200).json(query.results);
    } catch (error) {
        console.error("Error accessing Notion API", error);
        res.status(500).json({ error: "Error accessing Notion API" });
    }
}
