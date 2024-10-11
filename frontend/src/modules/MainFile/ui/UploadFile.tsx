import { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";

import { downloadFile } from "@/helpers/downloadFile";
import { fetchFile } from "@/modules/MainString/api/displayJson";
import Typography from "@/ui/Typography";
import toast from "react-hot-toast";
import { useUploadFile } from "../api/useUploadFile";
import { File } from "../types/file";
import { IRate, Table } from "./Table";
import test from "./test.json";

export const UploadFile = () => {
  const [file, setFile] = useState<File | null>();
  const [table, setTable] = useState<IRate[]>();

  const { mutateAsync, isPending, isSuccess, data } = useUploadFile();

  const addFile = useCallback((file: File) => {
    setFile(file);
  }, []);

  useEffect(() => {
    if (isSuccess) toast.success("Успешно загружен");
  }, [isSuccess]);

  const deleteFile = () => {
    setFile(null);
  };

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      acceptedFiles.forEach((file) => {
        addFile(file);
      });
    },
    [addFile]
  );
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
  });

  const handleSubmit = () => {
    if (file) mutateAsync({ file });
  };
  const handleDownloadCsv = useCallback(() => {
    if (data) downloadFile(data.data.result_csv);
  }, [data]);

  useEffect(() => {
    if (data && !isPending) {
      try {
        fetchFile(data.data.result).then((res: { names: IRate[] }) =>
          setTable(res.names)
        );
      } catch (e) {
        setTable(test.names);
      }
    }
  }, [data, isPending]);

  return (
    <div className="flex flex-col w-full">
      <div className="label text-gray-100">
        <span className="text-xl font-semibold prose-sm text-gray-100">
          Файл
        </span>
      </div>
      <div
        className=" border-2  text-gray-200 border-dashed border-gray-400 rounded-xl w-full h-[315px] py-8 px-6 flex flex-col items-center justify-center gap-4"
        {...getRootProps()}
      >
        {!isDragActive ? (
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="size-20"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m.75 12 3 3m0 0 3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z"
              />
            </svg>
          </div>
        ) : (
          <div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="size-20"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
              />
            </svg>
          </div>
        )}
        <p className="prose-md">Перенесите файл</p>
        <p className="prose-md">или</p>
        <div className="my-btn w-fit">
          <input className="hidden" {...getInputProps} />
          выберите файл
        </div>
      </div>
      {file && (
        <div>
          <div className="flex items-center justify-between gap-2 whitespace-nowrap bg-dark-bg text-sm w-fit py-1 my-2 px-2 rounded-lg text-white">
            {file?.path.toLowerCase().slice(0, 20)}
            <button
              className="hover:text-main-red transition"
              onClick={deleteFile}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="size-4"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M6 18 18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      )}
      <button
        className={`my-btn w-full mt-6 ${
          !file && "bg-stone-700 hover:bg-stone-700"
        }`}
        onClick={handleSubmit}
      >
        {isPending ? (
          <span className="loading"></span>
        ) : (
          "Получить стандартизацию"
        )}
      </button>
      {data && !isPending && (
        <div className="flex flex-col gap-4 mb-8">
          <Typography variant="h3" className="flex gap-2 text-lime-300 mt-10">
            Результат
          </Typography>
          <button className={`my-btn w-52`} onClick={handleDownloadCsv}>
            Скачать таблицу
          </button>
        </div>
      )}
      {table && <Table rates={table} />}
    </div>
  );
};
