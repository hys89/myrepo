import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

const connector = new ElasticsearchAPIConnector({
  // host: "http://ec2-47-129-205-236.ap-southeast-1.compute.amazonaws.com:9200",
  host: "http://esnode1:9200",
  index: "cv-transcriptions"
});

const config = {
  searchQuery: {
    search_fields: {
      generated_text: {},
      duration: {},
      age: {},
      gender: {},
      accent: {}
    },
    result_fields: {
      generated_text: {
        snippet: {}
      },
      duration: {
        raw: {}
      },
      age: {
        raw: {}
      },
      gender: {
        raw: {}
      },
      accent: {
        raw: {}
      }
    },
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox autocompleteSuggestions={true} />}
                  sideContent={
                    <div>
                      {wasSearched && <Sorting label={"Sort by"} sortOptions={[{name: "Relevance", value: "", direction: ""}]} />}
                    </div>
                  }
                  bodyContent={<Results />}
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
