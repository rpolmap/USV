/**
 * Providence Wiki Live Search Engine
 * Configured specifically for providence.fandom.com
 */
class ProvidenceWikiSearch {
  constructor() {
    this.wikiSubdomain = "providence";
    this.debounceTimer = null;
  }

  /**
   * Main search execution with a 300ms debounce to prevent API rate-limiting
   * @param {string} query - Text typed in the search box
   * @param {string} resultsContainerId - ID of the HTML element where results render
   */
  executeSearch(query, resultsContainerId = "searchResults") {
    clearTimeout(this.debounceTimer);
    const container = document.getElementById(resultsContainerId);
    if (!container) return;

    const cleanQuery = query.trim();

    if (!cleanQuery) {
      container.innerHTML = '<p style="color: #888; font-size: 0.9em;">Type to search the Providence wiki...</p>';
      return;
    }

    container.innerHTML = '<p style="color: #888; font-size: 0.9em;">Searching wiki...</p>';

    // Wait 300ms after user stops typing before making the network request
    this.debounceTimer = setTimeout(() => {
      this.fetchFandomResults(cleanQuery, container);
    }, 300);
  }

  /**
   * Fetches search results directly from the MediaWiki API on providence.fandom.com
   */
  async fetchFandomResults(query, container) {
    // MediaWiki search endpoint with origin=* to prevent CORS blocking on GitHub Pages
    const apiUrl = `https://${this.wikiSubdomain}.fandom.com/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&srlimit=10&format=json&origin=*`;

    try {
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      const results = data.query?.search || [];

      this.renderResults(results, container, query);
    } catch (error) {
      console.error("Fandom API Search Error:", error);
      container.innerHTML = '<p style="color: #d9534f; font-size: 0.9em;">Unable to connect to providence.fandom.com.</p>';
    }
  }

  /**
   * Renders the search API payload into HTML
   */
  renderResults(results, container, query) {
    if (results.length === 0) {
      container.innerHTML = `<p style="color: #888; font-size: 0.9em;">No results found on Providence Wiki for "${this.escapeHtml(query)}".</p>`;
      return;
    }

    container.innerHTML = results.map(item => {
      const articleUrl = `https://${this.wikiSubdomain}.fandom.com/wiki/${encodeURIComponent(item.title.replace(/ /g, '_'))}`;
      
      return `
        <div class="wiki-search-item" style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
          <a href="${articleUrl}" target="_blank" rel="noopener noreferrer" style="font-weight: bold; color: #4090ff; text-decoration: none; font-size: 1.05em;">
            ${item.title}
          </a>
          <p style="margin: 4px 0 0 0; font-size: 0.88em; color: #ccc; line-height: 1.4;">
            ${item.snippet}...
          </p>
        </div>
      `;
    }).join('');
  }

  escapeHtml(str) {
    return str.replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
  }
}

// Initialize instance
const providenceSearch = new ProvidenceWikiSearch();

/**
 * UI Hook Function
 * Attach this function to your search input element:
 * <input type="text" oninput="runProvidenceSearch(this.value, 'searchResults')">
 */
function runProvidenceSearch(inputValue, containerId = "searchResults") {
  providenceSearch.executeSearch(inputValue, containerId);
}
