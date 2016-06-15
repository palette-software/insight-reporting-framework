package main

import (
	log "github.com/palette-software/insight-tester/common/logging"
	dbconn "github.com/palette-software/insight-tester/common/db-connector"
	"os"
	"fmt"
)

const jobVersion = "0.8"
var noopHandler dbconn.ProcessRowFunc = func ([]string) error {
	// Do not do anything
	return nil
}

func main() {
	log.AddTarget(os.Stdout, log.LevelDebug)

	log.Infof("Starting Insight Reporting on version: %v", reporting_version + build_number)

	const config_file_path = "Config.yml"
	config, err := dbconn.ParseConfig(config_file_path)
	if err != nil {
		log.Fatalf("Failed to parse DB connector config file: %v! Error: %v", config_file_path, err)
	}

	dbconnector := &config.DbConnector
	defer dbconnector.CloseDB()

	//sql_statement := "select * from palette.threadinfo limit 1"
	//sql_statement := "select go_test.get_max_ts('go_test', 'threadinfo');"
	sql_statement := "select count(1) as c, process from palette.threadinfo where ts > now()::date - 2 group by process order by c;"
	//var count int64
	//var hostname string
	//
	//err = dbconnector.Query(sql_statement, func (columns []string) error {
	//	log.Debugf("Count: %d, Process: %s", count, hostname)
	//	return nil
	//}, &count, &hostname)
	//
	//if err != nil {
	//	log.Errorf("Failed to execute query: %v! Error: %v", sql_statement, err)
	//}

	//err = dbconnector.QueryValues(sql_statement, func (columns []string, values []reflect.Value) error {
	//	log.Debugf("Count: %d, Process: %s", values[0].Int(), values[1].String())
	//	return nil
	//})

	if err != nil {
		log.Errorf("Failed to execute query: %v! Error: %v", sql_statement, err)
	}

	err = logDataModelVersion(dbconnector)
	if err != nil {
		log.Error(err)
	}

	loadType := "" // FIXME: Need to get load type from somewhere!
	err = jobPiReportPThreadInfoNew(dbconnector, loadType)
	if err != nil {
		log.Error(err)
	}

	log.Info("Finished Insight Reporting.")
}

func logDataModelVersion(dbConnector *dbconn.DbConnector) error {
	queryDataModelVersion := "select first_value(version_number) over (order by id desc) as model_version from " +
		dbConnector.Schema + ".db_version_meta v limit 1"

	var version_number string

	err := dbConnector.Query(queryDataModelVersion, func (columns []string) error {
		log.Debugf("Data Model version number: %v", version_number)
		return nil
	}, &version_number)

	if err != nil {
		return fmt.Errorf("Failed to get Data Model version! Error: %v", err)
	}
	return nil
}

func jobPiReportPThreadInfoNew(dbConnector *dbconn.DbConnector, loadType string) error {
	jobName := "PI Report p_threadinfo_new"
	sql := "set application_name = 'Palette Insight - Talend " + jobName  +" : "+ jobVersion + " ' "

	err := dbConnector.Query(sql, noopHandler)
	if err != nil {
		return fmt.Errorf("Error in setting application name! Error: %v", err)
	}

	log.Info("Adding new partitions.")
	sql = "select " + dbConnector.Schema +".manage_partitions('" + dbConnector.Schema +"', 'p_threadinfo')"
	err = dbConnector.Query(sql, noopHandler)
	if err != nil {
		return fmt.Errorf("Error in managing partitions! Error: %v", err)
	}

	sql = "select "+ dbConnector.Schema + ".load_p_threadinfo('"+ dbConnector.Schema + "', '"
		+ loadType +"') "

	return nil
}