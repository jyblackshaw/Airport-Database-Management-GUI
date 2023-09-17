# p2app/engine/main.py
#
# ICS 33 Winter 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

from p2app import events as events
import sqlite3 as sql

#Engine communicates w/ UI, thru events.
#Receives event from UI, send back a message to UI.

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.db_conn = None #conn will be assigned after database open event.



    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        #In cases in which errors occur and there is no event specifically defined for it (e.g., when loading a continent fails), the engine should yield one ErrorEvent.

        # Database Events:
        if type(event) is events.QuitInitiatedEvent:
            yield self.Process_QuitInitiatedEvent(event)

        if type(event) is events.OpenDatabaseEvent:
            yield self.Process_OpenDataBaseEvent(event)

        if type(event) is events.CloseDatabaseEvent:
            yield self.Process_CloseDatabaseEvent(event)


        # Continent Events:
        if type(event) is events.StartContinentSearchEvent:
            yield_events = self.Process_StartContinentSearchEvent(event)
            for event in yield_events:
                yield event

        if type(event) is events.LoadContinentEvent:
            yield self.Process_LoadContinentEvent(event)

        if type(event) is events.SaveNewContinentEvent:
            yield self.Process_SaveNewContinentEvent(event)

        if type(event) is events.SaveContinentEvent:
            yield self.Process_SaveContinentEvent(event)


        #Country Events:
        if type(event) is events.StartCountrySearchEvent:
            yield_events = self.Process_StartCountrySearchEvent(event)
            for event in yield_events:
                yield event

        if type(event) is events.LoadCountryEvent:
            yield self.Process_LoadCountryEvent(event)

        if type(event) is events.SaveNewCountryEvent:
            yield self.Process_SaveNewCountryEvent(event)

        if type(event) is events.SaveCountryEvent:
            yield self.Process_SaveCountryEvent(event)

        
        #Region Events:
        if type(event) is events.StartRegionSearchEvent:
            yield_events = self.Process_StartRegionSearchEvent(event)
            for event in yield_events:
                yield event

        if type(event) is events.LoadRegionEvent:
            yield self.Process_LoadRegionEvent(event)

        if type(event) is events.SaveNewRegionEvent:
            yield self.Process_SaveNewRegionEvent(event)

        if type(event) is events.SaveRegionEvent:
            yield self.Process_SaveRegionEvent(event)


    #region Application Level Events
    def Process_QuitInitiatedEvent(self, event):
        if self.db_conn:
            self.db_conn.close()
        return events.EndApplicationEvent()

    def Process_OpenDataBaseEvent(self, event):
        yield_event = None

        # Establish Connection To Database:
        path_db = event.path()
        file_name = str(path_db).split("\\")[-1]
        try:
            if not file_name.endswith('.db'):
                raise Exception  #if not a db file, raise exception

            conn = sql.connect(path_db)
            conn.execute('PRAGMA foreign_keys = ON;')
            self.db_conn = conn
            yield_event = events.DatabaseOpenedEvent(path_db)
        except:
            yield_event = events.DatabaseOpenFailedEvent(f'Unable to connect to database {file_name}!')

        return yield_event

    def Process_CloseDatabaseEvent(self, event):
        if self.db_conn:
            self.db_conn.close()
        return events.DatabaseClosedEvent()

    #endregion


    # region Continent Events
    def Process_StartContinentSearchEvent(self, event):
        code = event.continent_code()
        name = event.name()
        search_query = None

        #OR query
        if (code and not name) or (name and not code):
            operator = 'AND'
            search_query = 'SELECT continent_id, continent_code, name ' \
                           'FROM continent '\
                           'WHERE continent_code = ? OR name = ?;'

        #AND query
        if name and code:
            search_query = 'SELECT continent_id, continent_code, name ' \
                           'FROM continent ' \
                           'WHERE continent_code = ? AND name = ?;'

        cursor = self.db_conn.execute(search_query, (code, name))
        query_data = cursor.fetchall()

        continent_result_events = []
        for continent_data in query_data:
            continent = self.Continent_NT_From_Query(continent_data)
            if continent:
                new_event = events.ContinentSearchResultEvent(continent)
                continent_result_events.append(new_event)

        return continent_result_events

    def Process_LoadContinentEvent(self, event):
        continent_id = event.continent_id()

        id_query = 'SELECT continent_id, continent_code, name ' \
                    'FROM continent ' \
                    'WHERE continent_id = ?;'

        cursor = self.db_conn.execute(id_query, [continent_id])
        query_data = cursor.fetchall()
        continent_data = query_data[0]
        continent = self.Continent_NT_From_Query(continent_data)

        return events.ContinentLoadedEvent(continent)

    def Process_SaveNewContinentEvent(self, event):
        new_continent = event.continent()
        new_code = new_continent.continent_code
        new_name = new_continent.name

        #Select Last ID in Continent Table:
        last_id_query = 'SELECT MAX(continent_id) ' \
                        'FROM continent' \

        cursor = self.db_conn.execute(last_id_query)
        new_id = str(cursor.fetchone()[0] + 1)  #Last id + 1

        #Insert New Continent:
        insert_query = 'INSERT INTO Continent (continent_code, name)' \
                       'VALUES (?, ?);'

        try:
            self.db_conn.execute(insert_query, [new_code, new_name])
            self.db_conn.commit()
            continent = events.Continent(new_id, new_code, new_name)

            return events.ContinentSavedEvent(continent)
        except:
            return events.SaveContinentFailedEvent('Was unable to add new Continent!')

    def Process_SaveContinentEvent(self, event):
        continent = event.continent()
        continent_id = continent.continent_id
        modified_code = continent.continent_code
        modified_name = continent.name

        update_query = 'UPDATE Continent SET continent_code = ?, name = ?' \
                       'WHERE continent_id = ?;'

        try:
            self.db_conn.execute(update_query, [modified_code, modified_name, continent_id])
            self.db_conn.commit()

            continent = events.Continent(continent_id, modified_code, modified_name)

            return events.ContinentSavedEvent(continent)
        except:
            return events.SaveContinentFailedEvent('Unable to save continent edits!')

    #Helper Functions:
    def Continent_NT_From_Query(self, continent_row_data):
        """Assumption is that it takes in data from a query for all values of a continent."""
        if len(continent_row_data) > 0:
            try:
                continent = events.Continent(continent_row_data[0], continent_row_data[1], continent_row_data[2])  # 'continent_id', 'continent_code', 'name'
                return continent
            except:
                return None

    # endregion


    # region Country Events
    def Process_StartCountrySearchEvent(self, event):
        country_code = event.country_code()
        country_name = event.name()
        country_query = None

        # OR query
        if (country_code and not country_name) or (country_name and not country_code):
            country_query = 'SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords ' \
                            'FROM country ' \
                            'WHERE country_code = ? OR name = ?;'

        # AND query
        if country_name and country_code:
            country_query = 'SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords ' \
                            'FROM country '\
                            'WHERE country_code = ? AND name = ?;'

        cursor = self.db_conn.execute(country_query, (country_code, country_name))
        query_data = cursor.fetchall()

        country_result_events = []
        for continent_data in query_data:
            country = self.Country_NT_From_Query(continent_data)
            if country:
                new_event = events.CountrySearchResultEvent(country)
                country_result_events.append(new_event)

        return country_result_events

    def Process_LoadCountryEvent(self, event):
        country_id = event.country_id()

        country_data_query = 'SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords ' \
                             'FROM country ' \
                             'WHERE country_id = ?;'

        cursor = self.db_conn.execute(country_data_query, [country_id])
        query_data = cursor.fetchall()
        country_data = query_data[0]
        country = self.Country_NT_From_Query(country_data)

        return events.CountryLoadedEvent(country)

    def Process_SaveNewCountryEvent(self, event):
        new_country = event.country()
        new_code = new_country.country_code
        new_name = new_country.name
        new_continent_id = new_country.continent_id
        new_wikipedia_link = new_country.wikipedia_link
        new_keywords = new_country.keywords

        # Select Last ID in Continent Table:
        last_id_query = 'SELECT MAX(country_id) ' \
                        'FROM Country'

        cursor = self.db_conn.execute(last_id_query)
        new_id = str(cursor.fetchone()[0] + 1)  # Last id + 1

        # Insert New Continent:
        insert_query = 'INSERT INTO Country (country_code, name, continent_id, wikipedia_link, keywords)' \
                       'VALUES (?, ?, ?, ?, ?);'

        try:
            self.db_conn.execute(insert_query, [new_code, new_name, new_continent_id, new_wikipedia_link, new_keywords])
            self.db_conn.commit()
            country = events.Country(new_id, new_code, new_name, new_continent_id, new_wikipedia_link, new_keywords)

            return events.CountrySavedEvent(country)
        except:
            return events.SaveCountryFailedEvent ('Was unable to add new Country!')

    def Process_SaveCountryEvent(self, event):
        country = event.country()
        country_id = country.country_id
        modified_code = country.country_code
        modified_name = country.name
        modified_continent_id = country.continent_id
        modified_wikipedia_link = country.wikipedia_link
        modified_keywords = country.keywords

        update_query = 'UPDATE Country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ?' \
                       'WHERE country_id = ?;'

        try:
            self.db_conn.execute(update_query, [modified_code, modified_name, modified_continent_id, modified_wikipedia_link, modified_keywords, country_id])
            self.db_conn.commit()

            country = events.Country(country_id, modified_code, modified_name, modified_continent_id, modified_wikipedia_link, modified_keywords)

            return events.CountrySavedEvent(country)
        except:
            return events.SaveCountryFailedEvent ('Unable to save country edits!')

    #Helper Functions:
    def Country_NT_From_Query(self, country_row_data):
        """Assumption is that it takes in data from a query for all values of a country, in correct order."""
        if len(country_row_data) > 0:
            try:
                country = events.Country(country_row_data[0], country_row_data[1], country_row_data[2], country_row_data[3], country_row_data[4], country_row_data[5])  # 'country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'
                return country
            except:
                return None

    # endregion



    # region Region Events

    def Process_StartRegionSearchEvent(self, event):
        region_code = event.region_code()
        local_code = event.local_code()
        region_name = event.name()

        #Attribute Counts:
        attributes = [region_code, local_code, region_name]
        attribute_count = 0

        for att in attributes:
            if att:
                attribute_count += 1

        cursor = None

        # 2 Attributes Query:
        if attribute_count == 2:
            if region_code and local_code and not region_name:
                region_query = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords ' \
                               'FROM region ' \
                               'WHERE region_code = ? AND local_code = ?;'
                cursor = self.db_conn.execute(region_query, (region_code, local_code))

            elif region_code and region_name and not local_code:
                region_query = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords ' \
                               'FROM region ' \
                               'WHERE region_code = ? AND name = ?;'
                cursor = self.db_conn.execute(region_query, (region_code, region_name))

            elif region_name and local_code and not region_code:
                region_query = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords ' \
                               'FROM region ' \
                               'WHERE local_code = ? AND name = ?;'
                cursor = self.db_conn.execute(region_query, (local_code, region_name))


        # 1 Attribute Query:
        elif attribute_count == 1:
            region_query = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords ' \
                           'FROM region ' \
                           'WHERE region_code = ? OR local_code = ? OR name = ?;'
            cursor = self.db_conn.execute(region_query, (region_code, local_code, region_name))


        #3 Attributes Query:
        elif attribute_count == 3:
            region_query = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords ' \
                           'FROM region ' \
                           'WHERE region_code = ? AND local_code = ? AND name = ?;'
            cursor = self.db_conn.execute(region_query, (region_code, local_code, region_name))

        query_data = cursor.fetchall()
        region_result_events = []
        for region_data in query_data:
            region = self.Region_NT_From_Query(region_data)
            if region:
                new_event = events.RegionSearchResultEvent (region)
                region_result_events.append(new_event)

        return region_result_events

    def Process_LoadRegionEvent(self, event):
        region_id = event.region_id()

        region_data_query = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords ' \
                            'FROM region ' \
                            'WHERE region_id = ?;'

        cursor = self.db_conn.execute(region_data_query, [region_id])
        query_data = cursor.fetchall()
        region_data = query_data[0]
        region = self.Region_NT_From_Query(region_data)

        return events.RegionLoadedEvent(region)

    def Process_SaveNewRegionEvent(self, event):
        new_region = event.region()

        new_region_code = new_region.region_code
        new_local_code = new_region.local_code
        new_name = new_region.name
        new_continent_id = new_region.continent_id
        new_country_id = new_region.country_id
        new_wikipedia_link = new_region.wikipedia_link
        new_keywords = new_region.keywords

        #Select Last ID in Continent Table:
        last_id_query = 'SELECT MAX(region_id) ' \
                        'FROM Region'

        cursor = self.db_conn.execute(last_id_query)
        new_id = str(cursor.fetchone()[0] + 1)  # Last id + 1

        # Insert New Continent:
        insert_query = 'INSERT INTO Region(region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) ' \
                       'VALUES (?, ?, ?, ?, ?, ?, ?);'

        try:
            self.db_conn.execute(insert_query, [new_region_code, new_local_code, new_name, new_continent_id, new_country_id, new_wikipedia_link, new_keywords])
            self.db_conn.commit()

            region = events.Region(new_id, new_region_code, new_local_code, new_name, new_continent_id, new_country_id, new_wikipedia_link, new_keywords)

            return events.RegionSavedEvent(region)
        except:
            return events.SaveRegionFailedEvent ('Was unable to add new Region!')

    def Process_SaveRegionEvent(self, event):
        region = event.region()
        region_id = region.region_id
        region_code = region.region_code
        local_code = region.local_code
        name = region.name
        continent_id = region.continent_id
        country_id = region.country_id
        wikipedia_link = region.wikipedia_link
        keywords = region.keywords

        update_query = 'UPDATE Region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ?' \
                       'WHERE country_id = ?;'

        try:
            self.db_conn.execute(update_query, [region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords, region_id])
            self.db_conn.commit()

            region = events.Region(region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)

            return events.RegionSavedEvent(region)
        except:
            return events.SaveRegionFailedEvent('Unable to save Region edits!')

    # Helper Functions:
    def Region_NT_From_Query(self, region_row_data):
        """Assumption is that it takes in data from a query for all 8 values of a region, in correct order."""
        if len(region_row_data) > 0:
            try:                      #region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords '
                region = events.Region(region_row_data[0], region_row_data[1],
                                       region_row_data[2], region_row_data[3],
                                       region_row_data[4], region_row_data[5],
                                       region_row_data[6], region_row_data[7])
                return region
            except:
                return None

    # endregion

