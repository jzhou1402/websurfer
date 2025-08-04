#!/bin/bash

# Web Scraping Interview Validator
# Compares candidate results with solution and provides fun feedback

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Emojis for fun
SURFER='🏄‍♂️'
WAVE='🌊'
CHECK='✅'
CROSS='❌'
TROPHY='🏆'
ROCKET='🚀'
LIGHTBULB='💡'

echo -e "${CYAN}${SURFER} NorCal Surf Adventures - Web Scraping Interview Validator ${WAVE}${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check if files exist
if [ ! -f "results.txt" ]; then
    echo -e "${RED}${CROSS} Error: results.txt not found!${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Make sure you've created results.txt with your scraped links${NC}"
    exit 1
fi

if [ ! -f "solution.txt" ]; then
    echo -e "${RED}${CROSS} Error: solution.txt not found!${NC}"
    echo -e "${YELLOW}${LIGHTBULB} The solution file should be provided by the interviewer${NC}"
    exit 1
fi

# Extract links from results.txt (remove comments and empty lines)
echo -e "${YELLOW}${LIGHTBULB} Analyzing your scraped links...${NC}"
grep -v '^#' results.txt | grep -v '^$' | sort -u > temp_results.txt

# Extract links from solution.txt (remove comments and empty lines)
grep -v '^#' solution.txt | grep -v '^$' | sort -u > temp_solution.txt

# Count total links
total_links=$(wc -l < temp_solution.txt)
found_links=$(wc -l < temp_results.txt)

# Find found and missing links
comm -12 temp_results.txt temp_solution.txt > found_links.txt
comm -23 temp_solution.txt temp_results.txt > missing_links.txt

found_count=$(wc -l < found_links.txt)
missing_count=$(wc -l < missing_links.txt)

# Calculate percentage
if [ $total_links -gt 0 ]; then
    percentage=$((found_count * 100 / total_links))
else
    percentage=0
fi

echo ""
echo -e "${GREEN}${CHECK} SCORING SUMMARY${NC}"
echo -e "${BLUE}===================${NC}"
echo -e "${GREEN}Total links available: ${total_links}${NC}"
echo -e "${GREEN}Links you found: ${found_count}${NC}"
echo -e "${RED}Links you missed: ${missing_count}${NC}"
echo -e "${YELLOW}Success rate: ${percentage}%${NC}"

echo ""
echo -e "${PURPLE}${TROPHY} PERFORMANCE ASSESSMENT${NC}"
echo -e "${BLUE}=======================${NC}"

# Performance assessment
if [ $percentage -ge 90 ]; then
    echo -e "${GREEN}${ROCKET} EXCELLENT! You're a web scraping master!${NC}"
    echo -e "${GREEN}You found almost all the links - impressive work!${NC}"
elif [ $percentage -ge 70 ]; then
    echo -e "${GREEN}${SURFER} GREAT JOB! You're getting the hang of this!${NC}"
    echo -e "${YELLOW}You found most links, but there's room for improvement.${NC}"
elif [ $percentage -ge 40 ]; then
    echo -e "${YELLOW}${WAVE} GOOD START! You're on the right track!${NC}"
    echo -e "${YELLOW}You found some links, but you're missing quite a few.${NC}"
else
    echo -e "${RED}${CROSS} NEEDS WORK! Keep practicing!${NC}"
    echo -e "${RED}You found very few links. Review the basics and try again!${NC}"
fi

echo ""
echo -e "${CYAN}${CHECK} LINKS YOU FOUND (${found_count})${NC}"
echo -e "${BLUE}========================${NC}"
if [ -s found_links.txt ]; then
    while IFS= read -r line; do
        echo -e "${GREEN}${CHECK} $line${NC}"
    done < found_links.txt
else
    echo -e "${RED}${CROSS} No links found!${NC}"
fi

echo ""
echo -e "${RED}${CROSS} LINKS YOU MISSED (${missing_count})${NC}"
echo -e "${BLUE}========================${NC}"
if [ -s missing_links.txt ]; then
    while IFS= read -r line; do
        echo -e "${RED}${CROSS} $line${NC}"
    done < missing_links.txt
else
    echo -e "${GREEN}${CHECK} No links missed! Perfect score!${NC}"
fi

echo ""
echo -e "${PURPLE}${LIGHTBULB} DIFFICULTY BREAKDOWN${NC}"
echo -e "${BLUE}====================${NC}"

# Count by difficulty level
static_count=$(grep -c "^/" temp_solution.txt)
external_count=$(grep -c "^https://" temp_solution.txt)
base64_count=$(grep -c "base64" temp_solution.txt 2>/dev/null || echo "0")

echo -e "${YELLOW}Static HTML links: ${static_count}${NC}"
echo -e "${YELLOW}External website links: ${external_count}${NC}"
echo -e "${YELLOW}Base64 encoded links: ${base64_count}${NC}"

echo ""
echo -e "${CYAN}${SURFER} TIPS FOR IMPROVEMENT${NC}"
echo -e "${BLUE}======================${NC}"

if [ $percentage -lt 40 ]; then
    echo -e "${YELLOW}${LIGHTBULB} Start with basic requests + BeautifulSoup${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Look for all <a> tags in the HTML${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Don't forget to check the href attributes${NC}"
elif [ $percentage -lt 70 ]; then
    echo -e "${YELLOW}${LIGHTBULB} Try using Selenium for dynamic content${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Look for JavaScript-generated content${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Check for user interactions (buttons, scrolls)${NC}"
elif [ $percentage -lt 90 ]; then
    echo -e "${YELLOW}${LIGHTBULB} Look for base64 encoded strings${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Check for hidden elements (CSS off-screen)${NC}"
    echo -e "${YELLOW}${LIGHTBULB} Consider timing and delays${NC}"
else
    echo -e "${GREEN}${TROPHY} You're doing great! Keep up the excellent work!${NC}"
fi

echo ""
echo -e "${BLUE}${WAVE} Happy scraping! ${SURFER}${NC}"

# Clean up temporary files
rm -f temp_results.txt temp_solution.txt found_links.txt missing_links.txt 