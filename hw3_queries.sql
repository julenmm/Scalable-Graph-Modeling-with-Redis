use graph;

#What is the sum of all book prices? Give just the sum
SELECT SUM(np.num_value) as 'Total Value of Books'
FROM graph.node
JOIN graph.node_props np on node.node_id = np.node_id
WHERE node.type = 'Book';

-- Total Value of Books
-- 253.45



#Who does spencer know? Give just their names.
SELECT DISTINCT np.string_value AS Name
FROM node n
JOIN node_props np ON n.node_id = np.node_id
JOIN edge e ON n.node_id = e.in_node OR n.node_id = e.out_node
WHERE n.type = 'Person'
AND np.string_value != 'Spencer'
AND e.type = 'Knows'
AND (
    e.in_node = (
        SELECT n.node_id
        FROM node n
        JOIN node_props np ON n.node_id = np.node_id
        WHERE n.type = 'Person' AND np.string_value = 'Spencer'
    )
    OR e.out_node = (
        SELECT n.node_id
        FROM node n
        JOIN node_props np ON n.node_id = np.node_id
        WHERE n.type = 'Person' AND np.string_value = 'Spencer'
    )
);
-- Name
-- Emily
-- Brendan


# What books did Spencer buy? Give title and price.
SELECT Book_Name, num_value as Price
FROM node_props np3
JOIN
    (SELECT np2.node_id AS id, np2.string_value AS Book_Name
    FROM node_props np2
    JOIN (
        SELECT e.out_node AS book_id
        FROM edge e
        WHERE e.type = 'bought'
            AND (
                e.in_node = (
                    SELECT no.node_id
                    FROM node no
                    JOIN node_props np ON np.node_id = no.node_id
                    WHERE np.string_value = 'Spencer'
                )
            )
    ) AS book_ids ON np2.node_id = book_ids.book_id
    WHERE np2.propkey = 'title') as book_names
ON np3.node_id = book_names.id
WHERE np3.propkey = 'price';

-- Book_Name, Price
-- Cosmos,17
-- Database Design,195




# Who knows each other? Give just a pair of names.
SELECT np1.string_value AS person1, np2.string_value AS person2
FROM edge e
JOIN node_props np1 ON e.out_node = np1.node_id AND np1.propkey = 'name'
JOIN node_props np2 ON e.in_node = np2.node_id AND np2.propkey = 'name'
WHERE e.type = 'knows';

-- Person 1, Person 2
-- Spencer,Emily
-- Brendan,Spencer
-- Emily,Spencer


# Demonstrate a simple recommendation engine by answering the following
# question with a SQL query: What books were purchased by people who Spencer
# knows? Exclude books that Spencer already owns. Warning: The algorithm we
# are using to make recommendations is conceptually simple, but you may find
# that your SQL query is rather complicated. This is why we need graph databases!

SELECT Distinct Book_Name
FROM node_props np3
JOIN (
    SELECT np2.node_id AS id, np2.string_value AS Book_Name
    FROM node_props np2
    JOIN (
        SELECT e.out_node AS book_id
        FROM edge e
        WHERE e.type = 'bought'
        AND e.in_node IN (
            SELECT DISTINCT knows_spencer_id
            FROM (
                SELECT n.node_id AS knows_spencer_id
                FROM node n
                JOIN node_props np ON n.node_id = np.node_id
                JOIN edge e ON n.node_id = e.in_node OR n.node_id = e.out_node
                WHERE n.type = 'Person'
                AND np.string_value != 'Spencer'
                AND e.type = 'Knows'
                AND (
                    e.in_node = (
                        SELECT n.node_id
                        FROM node n
                        JOIN node_props np ON n.node_id = np.node_id
                        WHERE n.type = 'Person' AND np.string_value = 'Spencer'
                    )
                    OR e.out_node = (
                        SELECT n.node_id
                        FROM node n
                        JOIN node_props np ON n.node_id = np.node_id
                        WHERE n.type = 'Person' AND np.string_value = 'Spencer'
                    )
                )
            ) AS spencer_friends
        )
    ) AS book_ids ON np2.node_id = book_ids.book_id
    WHERE np2.propkey = 'title'
) AS book_names ON np3.node_id = book_names.id
WHERE np3.propkey = 'price'
    AND np3.node_id NOT IN (SELECT np3.node_id as id_spencer_bough_already
FROM node_props np3
JOIN
    (SELECT np2.node_id AS id, np2.string_value AS Book_Name
    FROM node_props np2
    JOIN (
        SELECT e.out_node AS book_id
        FROM edge e
        WHERE e.type = 'bought'
            AND (
                e.in_node = (
                    SELECT no.node_id
                    FROM node no
                    JOIN node_props np ON np.node_id = no.node_id
                    WHERE np.string_value = 'Spencer'
                )
            )
    ) AS book_ids ON np2.node_id = book_ids.book_id
    WHERE np2.propkey = 'title') as book_names
ON np3.node_id = book_names.id
WHERE np3.propkey = 'price');

-- Book_Name
-- DNA and you




